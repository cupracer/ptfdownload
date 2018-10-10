# SUSE Program Temporary Fix (PTF) download helper
This script is intended to simplify the download of PTF packages.  
For more information on using PTFs, please visit the following support articles:

* Best practice for applying Program Temporary Fixes (PTFs)  
  https://www.suse.com/support/kb/doc/?id=7016640
  
* SLES 12: How to import suse_key for signed PTF packages  
  https://www.suse.com/support/kb/doc/?id=7016511

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
(see [test.py](https://github.com/cupracer/suse-ptf-utils/blob/master/test.py))

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
