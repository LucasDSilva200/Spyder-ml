<h1 align="center">Spyder-HTML</h1>

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
<img src="http://img.shields.io/static/v1?label=VERSION&message=0.3.6&color=blue&style=for-the-badge"/>
<img src="https://img.shields.io/github/license/accessmaker/Spyder-ml?style=for-the-badge"/>
</p>


A tool made to facilitate the analysis of html code.

<h2>INSTALL(git clone):</h2>

git clone https://github.com/accessmaker/Spyder-ml

python setup.py install


<h2>INSTALL(PIP):</h2>


pip install spyder-ml


<h2>USAGE:</h2>

spyderml [-h] [-t TARGET] [-f FILE] [--tags TAGS] [--comments]
               [--attribs ATTRIBS] [-o OUTPUT]

A tool made to facilitate the analysis of html code.

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Parameter that defines the target URL
                        http://example.com/index.html
  -f FILE, --file FILE  Parameter that defines target URLs
  --tags TAGS           Flag that defines which tags the program will bring
  --comments            Flag that brings the comments
  --attribs ATTRIBS     Flag that defines which attributes the application
                        will look for.
  -o OUTPUT, --output OUTPUT
                        Flag that defines in which file the command output
                        will be saved.

'Functionality': It searches the html document for specific things