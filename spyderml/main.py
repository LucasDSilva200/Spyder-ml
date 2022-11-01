#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import urllib3

from bs4 import BeautifulSoup as bs
from bs4 import Comment
from spyderml.lib.asciiarts import banner


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
    except requests.exceptions.MissingSchema:
        print(f"{target}:\nInvalid url\n http://?")
    except requests.exceptions.InvalidSchema:
        print(f"{target} ERROR")
    except:
        print(f"UNKNOWN ERROR")


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


class SpyderHtml:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(banner())
        texto = spyder_request(target=self.args.target)
        if self.args.comments and self.args.tags and self.args.attribs or self.args.comments and self.args.tags or \
                self.args.comments and self.args.attribs or self.args.attribs and self.args.tags:
            print("Os argumentos não podem ser executados juntos, escolha um por favor.")
            exit()
        elif self.args.tags:
            tags = tratar_objetos(objetos=self.args.tags)
            sopa_tags(documento=texto, objeto=tags)
        elif self.args.comments:
            sopa_comments(documento=texto)
        else:
            attr = tratar_objetos(objetos=self.args.attribs)
            sopa_attrs(documento=texto, objeto=attr)


def main():
    parser = argparse.ArgumentParser(description="Uma ferramenta feita para facilitar a análise de código html.")
    parser.add_argument('-t', '--target', type=str, required=True, help="Parâmetro que define a URL do alvo "
                                                         "\"http://example.com/index.html\"")
    parser.add_argument('--tags', type=str, help="Flag que define quais tags o programa vai trazer")

    parser.add_argument('--comments', help="Flag que traz os comentários", default=False, action='store_true', )

    parser.add_argument('--attribs', type=str, help="Flag que define quais atributos a aplicação irá procurar.")

    args = parser.parse_args()

    sp = SpyderHtml(args)
    sp.run()


if __name__ == '__main__':
    main()
