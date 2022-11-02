#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from build.lib.spyderml.main import spyder_request
from spyderml.lib.asciiarts import banner
from spyderml.lib.utils import tratar_objetos, sopa_tags, sopa_comments, sopa_attrs, tratar_arquivo


class SpyderHtml:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(banner())
        if self.args.file and self.args.target:
            print("Você só pode usar os argumentos (file e target) um por vez")

        elif self.args.file:
            alvos = tratar_arquivo(filepath=self.args.file)
            htmls = []
            for alvo in alvos:
                htmls.append(spyder_request(alvo))
                try:
                    for html in htmls:
                        if self.args.comments and self.args.tags and self.args.attribs or self.args.comments and self.args.tags or \
                                self.args.comments and self.args.attribs or self.args.attribs and self.args.tags:
                            print("Os argumentos não podem ser executados juntos, escolha um por favor.")
                            exit()
                        elif self.args.tags:
                            tags = tratar_objetos(objetos=self.args.tags)
                            sopa_tags(documento=html, objeto=tags)
                        elif self.args.comments:
                            sopa_comments(documento=html)
                        else:
                            attr = tratar_objetos(objetos=self.args.attribs)
                            sopa_attrs(documento=html, objeto=attr)



                except AttributeError:
                    pass
        else:
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

    parser.add_argument('-t', '--target', type=str, help="Parâmetro que define a URL do alvo "
                                                         "\"http://example.com/index.html\"")
    parser.add_argument('-f', '--file', type=str, help="Parâmetro que define as URLs dos alvos")

    parser.add_argument('--tags', type=str, help="Flag que define quais tags o programa vai trazer")

    parser.add_argument('--comments', help="Flag que traz os comentários", default=False, action='store_true', )

    parser.add_argument('--attribs', type=str, help="Flag que define quais atributos a aplicação irá procurar.")

    args = parser.parse_args()

    sp = SpyderHtml(args)
    sp.run()


if __name__ == '__main__':
    main()
