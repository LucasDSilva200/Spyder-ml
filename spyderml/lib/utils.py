import requests
import urllib3

from bs4 import BeautifulSoup as bs
from bs4 import Comment

from spyderml.lib.file import save_output


def tratar_objetos(objetos: str):
    if "," in objetos:
        objetos = objetos.split(',')
        return objetos
    return objetos


def spyder_request(target):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        r = requests.get(target)
        return r
    except requests.exceptions.SSLError:
        print(f"{target}:\nErro de ssl")
        exit()
    except requests.exceptions.MissingSchema:
        print(f"{target}:\nInvalid url\n http://?")
        exit()
    except requests.exceptions.InvalidSchema:
        print(f"{target} ERROR")
        exit()
    except:
        print("UNKNOWN ERROR")
        exit()


def sopa_tags(documento, objeto, file=None):
    html = bs(documento.content, 'html.parser')
    resultados = html.find_all(objeto)
    for resultado in resultados:
        if file is not None:
            save_output(filename=file, text=resultado)
        print(resultado)


def sopa_comments(documento, file=None):
    html = bs(documento.content, 'html.parser')
    comentarios = html.find_all(string=lambda text: isinstance(text, Comment))
    for comentario in comentarios:
        if file is not None:
            save_output(filename=file, text=comentario)
        print(comentario)


def sopa_attrs(documento, objeto, file=None):
    html = bs(documento.content, 'html.parser')
    if type(objeto) == list:
        for o in objeto:
            print(o)
            for atributo in html.select(f"[{o}]"):
                if file is not None:
                    save_output(filename=file, text=atributo)
                print(atributo)
    else:
        for atributo in html.select(f"[{objeto}]"):
            if file is not None:
                save_output(filename=file, text=atributo)
            print(atributo)
