<h1 align="center">Spyder-HTML</h1>

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
<img src="http://img.shields.io/static/v1?label=VERSION&message=1.2.0&color=blue&style=for-the-badge"/>
<img src="https://img.shields.io/github/license/accessmaker/Spyder-ml?style=for-the-badge"/>
</p>


A tool made to facilitate the analysis of html code.

<h2>INSTALL(git clone):</h2>

git clone https://github.com/accessmaker/Spyder-ml

python setup.py install


<h2>INSTALL(PIP):</h2>


pip install spyder-ml


<h2>USAGE:</h2>

spyderml [-h] [-t TARGET | -f FILE | --update]
         [--tags TAGS | --comments | --attribs ATTRIBS | --getjs | --techs]
         [-o OUTPUT]

A tool made to facilitate the analysis of html code.

options:<br>
  -h, --help            show this help message and exit<br>
  -t TARGET, --target TARGET<br>
                        Parameter that defines the target URL<
                        http://example.com/index.html <br>
  -f FILE, --file FILE  Parameter that defines target URLs<br>
  --update              Flag responsible for updating the database.<br>
  --tags TAGS           Flag that defines which tags the program will bring<br>
  --comments            Flag that brings the comments<br>
  --attribs ATTRIBS     Flag that defines which attributes the application
                        will look for.<br>
  --getjs               Flag that brings all JS files from the page.<br>
  --techs               Flag trying to discover the technologies of the page.<br>
  -o OUTPUT, --output OUTPUT
                        Flag that defines in which file the command output
                        will be saved.<br>

'Functionality': It searches the html document for specific things