import requests
import urllib3

from bs4 import BeautifulSoup as bs
from bs4 import Comment


def tratar_objetos(objetos: str):
    if "," in objetos:
        objetos = objetos.split(',')
        return objetos
    return objetos


def tratar_arquivo(filepath):
    try:
        with open(filepath, 'r') as file:
            linhas = file.read()
            linhas = linhas.strip()
        linhas = linhas.split('\n')
        return linhas
    except FileNotFoundError:
        print(f"Arquivo não encontrado({filepath})")
        exit()


def spyder_request(target):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        r = requests.get(target)
        return r
    except requests.exceptions.SSLError:
        return f"{target}:\nErro de ssl"
    except requests.exceptions.MissingSchema:
        return f"{target}:\nInvalid url\n http://?"
    except requests.exceptions.InvalidSchema:
        return f"{target} ERROR"
    except:
        return "UNKNOWN ERROR"


def sopa_tags(documento, objeto):
    html = bs(documento.content, 'html.parser')
    resultados = html.find_all(objeto)
    for resultado in resultados:
        print(resultado)


def sopa_comments(documento):
    html = bs(documento.content, 'html.parser')
    comentarios = html.find_all(string=lambda text: isinstance(text, Comment))
    for commentario in comentarios:
        print(commentario)


def sopa_attrs(documento, objeto):
    html = bs(documento.content, 'html.parser')
    if len(objeto) > 1:
        for o in objeto:
            for atributo in html.select(f"[{o}]"):
                print(atributo)
    else:
        for atributo in html.select(f"[{objeto}]"):
            print(atributo)
