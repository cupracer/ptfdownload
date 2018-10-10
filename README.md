# suse-ptf-utils

## Command-line interface
```
# ./PTFload.py -h
usage: PTFload.py [-d <outputdir>] [-u <url>] [-i] [-v]

  -d: use specified download directory
  -u: PTF base URL to use
  -i: include  optional packages (src, debuginfo, debugsource)
  -v: verbose output
```

## Module
(see test.py)

```
#!/usr/bin/python

from PTFload import doPtfDownload

outputdir = './'
url = ''
username = ''
password = ''
includeOptional = False
verbose = True

doPtfDownload(outputdir, url, username, password, includeOptional, verbose)
```
