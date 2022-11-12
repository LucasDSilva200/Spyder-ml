#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from spyderml.lib.asciiarts import banner
from spyderml.lib.utils import spyder_request, treat_objects, soup_tags, soup_comments, soup_attrs
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
                            tags = treat_objects(objects=self.args.tags)
                            soup_tags(document=html, object=tags, file=self.args.output)
                        elif self.args.comments:
                            soup_comments(document=html, file=self.args.output)
                        else:
                            attr = treat_objects(objects=self.args.attribs)
                            soup_attrs(document=html, object=attr, file=self.args.output)



                except AttributeError:
                    pass
        else:
            texto = spyder_request(target=self.args.target)
            if self.args.comments and self.args.tags and self.args.attribs or self.args.comments and self.args.tags or \
                    self.args.comments and self.args.attribs or self.args.attribs and self.args.tags:
                print("Os argumentos não podem ser executados juntos, escolha um por favor.")
                exit()
            elif self.args.tags:
                tags = treat_objects(objects=self.args.tags)
                soup_tags(document=texto, object=tags, file=self.args.output)
            elif self.args.comments:
                soup_comments(document=texto, file=self.args.output)
            else:
                attr = treat_objects(objects=self.args.attribs)
                soup_attrs(document=texto, object=attr, file=self.args.output)


def main():
    parser = argparse.ArgumentParser(description="A tool made to facilitate the analysis of html code.")

    parser.add_argument('-t', '--target', type=str, help="Parameter that defines the target URL "
                                                         "http://example.com/index.html")
    parser.add_argument('-f', '--file', type=str, help="Parameter that defines target URLs")

    parser.add_argument('--tags', type=str, help="Flag that defines which tags the program will bring")

    parser.add_argument('--comments', help="Flag that brings the comments", default=False, action='store_true', )

    parser.add_argument('--attribs', type=str, help="Flag that defines which attributes the application will look for.")

    parser.add_argument('-o', '--output', type=str, help="Flag that defines in which file the command output will be "
                                                         "saved.")

    args = parser.parse_args()

    sp = SpyderHtml(args)
    sp.run()


if __name__ == '__main__':
    main()
