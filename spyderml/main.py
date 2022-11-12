#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from spyderml.lib.asciiarts import banner
from spyderml.lib.utils import spyder_request, tratar_objetos, sopa_tags, sopa_comments, sopa_attrs
from spyderml.lib.file import open_file


class SpyderHtml:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(banner())
        if self.args.file and self.args.target:
            print("Você só pode usar os argumentos (file e target) um por vez")

        elif self.args.file:
            alvos = open_file(filepath=self.args.file)
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
                            sopa_tags(documento=html, objeto=tags, file=self.args.output)
                        elif self.args.comments:
                            sopa_comments(documento=html, file=self.args.output)
                        else:
                            attr = tratar_objetos(objetos=self.args.attribs)
                            sopa_attrs(documento=html, objeto=attr, file=self.args.output)



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
                sopa_tags(documento=texto, objeto=tags, file=self.args.output)
            elif self.args.comments:
                sopa_comments(documento=texto, file=self.args.output)
            else:
                attr = tratar_objetos(objetos=self.args.attribs)
                sopa_attrs(documento=texto, objeto=attr, file=self.args.output)


def main():
    parser = argparse.ArgumentParser(description="Uma ferramenta feita para facilitar a análise de código html.")

    parser.add_argument('-t', '--target', type=str, help="Parâmetro que define a URL do alvo "
                                                         "\"http://example.com/index.html\"")
    parser.add_argument('-f', '--file', type=str, help="Parâmetro que define as URLs dos alvos")

    parser.add_argument('--tags', type=str, help="Flag que define quais tags o programa vai trazer")

    parser.add_argument('--comments', help="Flag que traz os comentários", default=False, action='store_true', )

    parser.add_argument('--attribs', type=str, help="Flag que define quais atributos a aplicação irá procurar.")

    parser.add_argument('-o', '--output', type=str, help="Flag que define em qual arquivo vai ser salvo a saída do "
                                                         "comando.")

    args = parser.parse_args()

    sp = SpyderHtml(args)
    sp.run()


if __name__ == '__main__':
    main()
