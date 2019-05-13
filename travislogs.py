#!/usr/bin/python2.7

import sys
import os
import json
import requests

# travislogger.py by root4loot (github.com/root4loot/travislogs)
# Grabs build logs from travis-ci.org and travis-ci.com
# results are stored to ./org and ./com/
#
# Usage: python travislogs.py <organization>

def req(url):
	r=requests.get(url, headers={'Travis-API-Version': '3'})
	return r.json()

def main(owner):
	exts = ['org', 'com']

	for eIndex, ext in enumerate(exts):
		repos = req("https://api.travis-ci."+ext+"/owner/"+owner+"/repos?limit=0")
		activeRepos = 0

		try:
			for repo in repos['repositories']:
				if repo['active']:
					activeRepos += 1

			if activeRepos == 0:
				print("No active repo in endpoint ["+str(eIndex+1)+"/"+str(len(exts))+"] (travis-ci."+ext)+")"

			for rIndex, repo in enumerate(repos['repositories']):
				repoID = repo['id']
				slug = repo['slug']
				isActive = repo['active']				

				if isActive == True:
					builds = req("https://api.travis-ci."+ext+"/repo/"+str(repoID)+"/builds?limit=0")


					buildsC = len(builds['builds'])
					for bIndex, build in enumerate(builds['builds']):
						if not os.path.exists(ext+'/'+slug+'/'+'jobs'):
							os.makedirs(ext+'/'+slug+'/'+'jobs')


						jobsC = len(build['jobs'])
						for jIndex, job in enumerate(build['jobs']):
							sys.stdout.write("Travis Endpoint: ["+str(eIndex+1)+"/"+str(len(exts))+"] Active Repo: ["+str(rIndex+1)+"/"+str(activeRepos)+"] Build: ["+str(bIndex+1)+"/"+str(buildsC)+"] Job: ["+str(jIndex+1)+"/"+str(jobsC)+"]\r")
							sys.stdout.flush()

							jobId = job['id']
							if not os.path.exists(ext+'/'+slug+'/jobs/'+str(jobId)+".txt"):
								f=open(ext+'/'+slug+'/jobs/'+str(jobId)+".txt","w+")
								
								r=requests.get("https://api.travis-ci."+ext+"/job/"+str(jobId)+"/log.txt", 
									headers={'Travis-API-Version': '3'})
								f.write(r.content)
								f.close()
		except:
			print("Something went wrong. Make sure the organization name is correct")
			
	print("\033[1mDone\033[0m\n")

if __name__== "__main__":
	try:
		owner = sys.argv[1]
		print("")
		main(owner)
	except:
		print("\n\033[94mtravislogs.py by root4loot (github.com/root4loot/travislogs)\033[0m")
		print("\033[1musage: python travislogs.py <organization>\033[0m\n")