```
          ``                                                              
     `:    .//-.   -:-`                                                   
   `  -s`   `odo-`  .y+.                                                  
   /   od+`   .dmy+.  omo-                                                
   +:  `hNy.   -sMNs-``/Nd+.        ▄▄· ▄▄▌   ▄▄▄· ▄▄▌ ▐ ▄▌▄▄▌  ▄▄▄ .▄▄▄  
   .d/` .hMd/-` .yMMm/``-yMh.      ▐█ ▌▪██•  ▐█ ▀█ ██· █▌▐███•  ▀▄.▀·▀▄ █·
   `oN+  -NMh:. .-NMMy. `-mMm:`    ██ ▄▄██▪  ▄█▀▀█ ██▪▐█▐▐▌██▪  ▐▀▀▪▄▐▀▀▄ 
    -MN. `/mMm+. .ohNNs. `.sMN/`   ▐███▌▐█▌▐▌▐█ ▪▐▌▐█▌██▐█▌▐█▌▐▌▐█▄▄▌▐█•█▌
    -dMo` `yNMm:`  `-hM+.  `sNh.   ·▀▀▀ .▀▀▀  ▀  ▀  ▀▀▀▀ ▀▪.▀▀▀  ▀▀▀ .▀  ▀
    `.dM/  `-dMh-`   -Nm/.   :d+                                          
     -mMd:`  :mN+`    -sy`    `:                                          
      +dMs`   .ss`      /.      `  		by truerandom
       .mN:    .o-       `         
        .+s      -`                
          .:                       
                                   
```

# Crawleet
Web Recon & Exploitaition Tool.  
It detects and exploit flaws in:
* Drupal
* Joomla
* Magento
* Moodle
* OJS
* Struts
* Wordpress 

And enumerates themes, plugins and sensitive files\
Also detects:
* Crypto mining scripts
* Malware

The tool is extensible using xml files.

## Installation
1. Use `linuxinstaller.sh`
2. Or use pip to install the following libraries:
	* requests
	* anytree
	* lxml
## Usage
* `python -u <starting url>`
* `python -l <file with sites>`

## Report
It generates reports in the following formats
* html
* txt
* xml
	
## All Options
```
Options:
  -h, --help            show this help message and exit
  -a USERAGENT,		--user-agent=USERAGENT
                        Set User agent
  -b, --brute           Enable Bruteforcing for resource discovery
  -c CFGFILE,		--cfg=CFGFILE
                        External tools config file
  -d DEPTH,		--depth=DEPTH
                        Crawling depth
  -e EXCLUDE,		--exclude=EXCLUDE
                        Resources to exclude (comma delimiter)
  -f,			--redirects       
			Follow Redirects
  -i TIME,		--time=TIME
			Delay between requests 
  -k COOKIES,		--cookies=COOKIES
                        Set cookies
  -l SITELIST,		--site-list=SITELIST
                        File with sites to scan (one per line)
  -m,			--color
			Colored output
  -n TIMEOUT,		--timeout=TIMEOUT
                        Timeout for request
  -o OUTPUT,		--output=OUTPUT
                        Output formats txt,html
  -p PROXY, 		--proxy=PROXY
                        Set Proxies "http://ip:port;https://ip:port"
  -r, 			--runtools
			Run external tools
  -s, 			--skip-cert
			Skip Cert verifications
  -t,			--tor
			Use tor
  -u URL,		--url=URL
			Url to analyze
  -v,			--verbose
			Verbose mode
  -w WORDLIST, 		--wordlist=WORDLIST
                        Bruteforce wordlist
  -x EXTENSIONS,	--exts=EXTENSIONS
                        Extensions to use for bruteforce
  -y, 			--backups
			Search for backup files
  -z MAXFILES,		--maxfiles=MAXFILES
                        Max files in the site to analyze
  --datadir=DATADIR	data directory
```
