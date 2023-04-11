<h1 align="center">Spyder-HTML</h1>

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
<img src="http://img.shields.io/static/v1?label=VERSION&message=2.1.4&color=blue&style=for-the-badge"/>
<img src="https://img.shields.io/github/license/accessmaker/Spyder-ml?style=for-the-badge"/>
</p>

A tool made to facilitate the analysis of html code.

<h2>INSTALL(git clone):</h2>

git clone <https://github.com/accessmaker/Spyder-ml>

python setup.py install

<h2>INSTALL(PIP):</h2>

pip install spyder-ml

<h2>USAGE:</h2>

spyderml       [-h] [-t TARGET] [--tr TR] [--update]
               [--tags TAGS | --comments | --attribs ATTRIBS | --getjs | --techs | --geturls | --html | --jsr]
               [-o OUTPUT] [-C COOKIE] [-A AGENT] [-hf HEADERSFILE] [-S]
               [-w WORKERS] [--domain DOMAIN] [--cache] [--proxy PROXY]
               [-D DATA [DATA ...]]

A tool made to facilitate the analysis of html code.

options:<br>
  -h, --help            show this help message and exit<br>
  -t TARGET, --target TARGET<br>
                        Parameter that defines the target URL<
                        <http://example.com/index.html> <br>
  --tr TR               Type of request(POST or GET(Default)).
  --update              Flag responsible for updating the database.<br>
  --tags TAGS           Flag that defines which tags the program will bring<br>
  --comments            Flag that brings the comments<br>
  --attribs ATTRIBS     Flag that defines which attributes the application
                        will look for.<br>
  --getjs               Flag that brings all JS files from the page.<br>
  --techs               Flag trying to discover the technologies of the page.<br>
  --geturls             This flag takes all the target's urls and tries to
                        access them.<br>
  --html                This Flag results in all the page's html code.<br>
  --jsr                 Makes a request that returns a JSON.<br>
  -o OUTPUT, --output OUTPUT
                        Flag that defines in which file the command output
                        will be saved.<br>
  -C COOKIE, --cookie COOKIE
                        Cookie to send with the request<br>
  -A AGENT, --agent AGENT
                        User-Agent to send with the request<br>
  -hf HEADERSFILE, --headersfile HEADERSFILE
                        Parameter that passes an HTTP request header file to
                        be scanned.<br>
  -S, --spider          flag to run spider<br>
  -w WORKERS, --workers WORKERS
                        Defines the number of workers.<br>
  --domain DOMAIN       Defines the domain of the web crawler.<br>
  --cache               Defines whether to create cache or not (default:
                        false).<br>
  --proxy PROXY         Defines the proxy that will be used (Which can be
                        passed tor or burpsuite to use these two default
                        proxies).<br>
  -D DATA [DATA ...], --data DATA [DATA ...]
                        Data to send with the request in format key1:value1
                        key2:value2 key3:value3...<br>

'Functionality': It searches the html document for specific things
