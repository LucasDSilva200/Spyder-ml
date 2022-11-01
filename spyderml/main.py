#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import urllib3

from bs4 import BeautifulSoup as bs
from spyderml.lib.asciiarts import banner


def tratar_tags(tags: str):
    if "," in tags:
        tags = tags.split(',')
        return tags
    return tags


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


def sopa(documento, objeto):
    html = bs(documento.content, 'html.parser')
    resultados = html.find_all(objeto)
    for resultado in resultados:
        print(resultado)


class SpyderHtml:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(banner())
        tags = tratar_tags(self.args.tags)
        texto = spyder_request(target=self.args.target)
        sopa(documento=texto, objeto=tags)


def main():
    parser = argparse.ArgumentParser(description="Uma ferramenta feita para facilitar a análise de código html.")
    parser.add_argument('-t', '--target', type=str, help="Parâmetro que define a URL do alvo "
                                                         "\"http://example.com/index.html\"")
    parser.add_argument('--tags', help="Define quais tags o programa vai trazer")

    args = parser.parse_args()

    sp = SpyderHtml(args)
    sp.run()


if __name__ == '__main__':
    main()
