<h1 align="center">Spyder-HTML</h1>

<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
<img src="http://img.shields.io/static/v1?label=VERSION&message=0.3.5&color=blue&style=for-the-badge"/>
<img src="https://img.shields.io/github/license/accessmaker/Spyder-ml?style=for-the-badge"/>
</p>



Uma ferramenta feita para facilitar a análise de código html.

<h2>INSTALL(git clone):</h2>

git clone https://github.com/accessmaker/Spyder-ml

python setup.py install


<h2>INSTALL(PIP):</h2>


pip install spyder-ml


<h2>USAGE:</h2>

spyderml -h
usage: spyderml [-h] -t TARGET [--tags TAGS] [--comments] [--attribs ATTRIBS] [-o OUTPUT]


Spyder-ml by:Lucas dSilva

options:
  <br>-h, --help            show this help message and exit
  <br>-t TARGET, --target TARGET
                        Parâmetro que define a URL do alvo "http://example.com/index.html"
  <br>--tags TAGS           Define quais tags o programa vai trazer
  <br>--comments            Flag que traz os comentários
  <br>--attribs ATTRIBS     Flag que define quais atributos a aplicação irá procurar.
  <br>-o OUTPUT, --output OUTPUT
                        Flag que define em qual arquivo vai ser salvo a saída
                        do comando.
<h2>FUNCTIONALITY</h2>

'Funcionalidade': Ele busca no documento html por coisas especificas
