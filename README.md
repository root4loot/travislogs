A simple script to grab build logs from Travis CI (travis-ci.org and travis-ci.com)

### Usage
Requires Python 2.7
```
./travislogs.py <organization>
```

Build logs are stored in org/organization and com/organization

### Example
```
./travislogs.py spotify
...
Travis Endpoint: [1/2] Active Repo: [1/60] Build: [5/100] Job: [1/1]
```

```
cat org/spotify/dockerfile-maven/jobs/432353567.txt
```

Tip: Use [ripgrep](https://github.com/BurntSushi/ripgrep) to speed up the grepping process
```
rg -ia 'password=' -j 12 --no-line-number --pretty
```