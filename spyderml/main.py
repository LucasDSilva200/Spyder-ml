#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from spyderml.lib.asciiarts import banner
from spyderml.lib.utils import spyder_request, treat_objects, soup_tags, soup_comments, soup_attrs, get_js, \
    detect_technologies, update_database
from spyderml.lib.file import open_file

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


class SpyderHtml:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(banner())

        if self.args['file']:
            targets = open_file(filepath=self.args['file'])
            htmls = []
            for target in targets:
                if self.args['techs']:
                    detect_technologies(url=target, filepath=self.args['output'])
                else:
                    htmls.append(spyder_request(target))
            try:
                for html in htmls:
                    if self.args['tags']:
                        tags = treat_objects(objects=self.args['tags'])
                        soup_tags(document=html, object=tags, file=self.args['output'])
                    elif self.args['comments']:
                        soup_comments(document=html, file=self.args['output'])
                    elif self.args['getjs']:
                        get_js(url=self.args['target'], document=html, file=self.args['output'])
                    else:
                        attr = treat_objects(objects=self.args['attribs'])
                        soup_attrs(document=html, object=attr, file=self.args['output'])

            except AttributeError:
                pass

        elif self.args['update']:
            update_database()

        else:
            text = spyder_request(target=self.args['target'])
            if self.args['tags']:
                tags = treat_objects(objects=self.args['tags'])
                soup_tags(document=text, object=tags, file=self.args['output'])
            elif self.args['comments']:
                soup_comments(document=text, file=self.args['output'])
            elif self.args['getjs']:
                get_js(url=self.args['target'], document=text, file=self.args['output'])
            elif self.args['techs']:
                detect_technologies(url=self.args['target'], filepath=self.args['output'])
            else:
                attr = treat_objects(objects=self.args['attribs'])
                soup_attrs(document=text, object=attr, file=self.args['output'])


def main():
    parser = argparse.ArgumentParser(description="A tool made to facilitate the analysis of html code.")

    group_target = parser.add_mutually_exclusive_group()

    group_action = parser.add_mutually_exclusive_group()

    group_target.add_argument('-t', '--target', type=str, help="Parameter that defines the target URL "
                                                               "http://example.com/index.html")
    group_target.add_argument('-f', '--file', type=str, help="Parameter that defines target URLs")

    group_target.add_argument('--update',help='Flag responsible for updating the database.',
                              default=False, action='store_true')
    group_action.add_argument('--tags', type=str, help="Flag that defines which tags the program will bring")

    group_action.add_argument('--comments', help="Flag that brings the comments", default=False, action='store_true', )

    group_action.add_argument('--attribs', type=str,
                              help="Flag that defines which attributes the application will look for.")

    group_action.add_argument('--getjs', help='Flag that brings all JS files from the page.',
                              default=False, action='store_true')
    group_action.add_argument('--techs', help='Flag trying to discover the technologies of the page.',
                              default=False, action='store_true')
    parser.add_argument('-o', '--output', type=str, help="Flag that defines in which file the command output will be "
                                                        "saved.")

    args = vars(parser.parse_args())

    if not any(args.values()):
        parser.error('No arguments provided.')

    sp = SpyderHtml(args)
    sp.run()


if __name__ == '__main__':
    main()
