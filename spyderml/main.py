#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from spyderml.lib.asciiarts import banner
from spyderml.lib.spidercrawler import get_all_urls, WebCrawling
from spyderml.lib.utils import spyder_request, treat_objects, soup_tags, soup_comments, soup_attrs, get_js, \
    detect_technologies, update_database, print_html
from spyderml.lib.file import open_file, open_headers_file

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


class TreatArguments:
    def __init__(self, args):
        self.args = args

    def run(self):
        print(banner())
        try:
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
                        elif self.args['geturls']:
                            get_all_urls(document=html, file=self.args['output'])
                        else:
                            attr = treat_objects(objects=self.args['attribs'])
                            soup_attrs(document=html, object=attr, file=self.args['output'])

                except AttributeError:
                    pass

            elif self.args['update']:
                update_database()

            else:
                if self.args['headersfile'] is not None:
                    headers = open_headers_file(headers_file=self.args['headersfile'])
                    html_document = spyder_request(target=self.args['target'],
                                                   headersfile=headers)
                else:
                    html_document = spyder_request(target=self.args['target'], useragent=self.args['agent'],
                                                   cookie=self.args['cookie'])

                if self.args['tags']:
                    tags = treat_objects(objects=self.args['tags'])
                    soup_tags(document=html_document, object=tags, file=self.args['output'])
                elif self.args['comments']:
                    soup_comments(document=html_document, file=self.args['output'])
                elif self.args['getjs']:
                    get_js(url=self.args['target'], document=html_document, file=self.args['output'])
                elif self.args['techs']:
                    detect_technologies(url=self.args['target'], filepath=self.args['output'])
                elif self.args['geturls']:
                    if self.args['spider']:
                        wc = WebCrawling(permission=self.args['spider'], workers=self.args['workers'],
                                         filepath=self.args['output'], domain=self.args['domain'])
                        wc.pre_queue_to_crawling(url=self.args['target'])
                    else:
                        get_all_urls(document=html_document, file=self.args['output'])
                elif self.args['html']:
                    print_html(document=html_document, file=self.args['output'])
                else:
                    attr = treat_objects(objects=self.args['attribs'])
                    soup_attrs(document=html_document, object=attr, file=self.args['output'])
        except KeyboardInterrupt:
            print("\nClossing...\n")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="A tool made to facilitate the analysis of html code.")

    group_target = parser.add_mutually_exclusive_group()

    group_action = parser.add_mutually_exclusive_group()

    group_target.add_argument('-t', '--target', type=str, help="Parameter that defines the target URL "
                                                               "http://example.com/index.html")
    group_target.add_argument('-f', '--file', type=str, help="Parameter that defines target URLs")

    group_target.add_argument('--update', help='Flag responsible for updating the database.',
                              default=False, action='store_true')
    group_action.add_argument('--tags', type=str, help="Flag that defines which tags the program will bring")

    group_action.add_argument('--comments', help="Flag that brings the comments", default=False, action='store_true', )

    group_action.add_argument('--attribs', type=str,
                              help="Flag that defines which attributes the application will look for.")

    group_action.add_argument('--getjs', help='Flag that brings all JS files from the page.',
                              default=False, action='store_true')
    group_action.add_argument('--techs', help='Flag trying to discover the technologies of the page.',
                              default=False, action='store_true')
    group_action.add_argument('--geturls', help='This flag takes all the target\'s urls and tries to access them.',
                              default=False, action='store_true')

    group_action.add_argument('--html', help='This Flag results in all the page\'s html code.',
                              default=False, action='store_true')

    parser.add_argument('-o', '--output', type=str,
                        help="Flag that defines in which file the command output will be "
                        "saved.")
    parser.add_argument('-C', '--cookie', type=str, help="Cookie to send with the request",
                        default='')
    parser.add_argument('-A', '--agent', type=str, help="User-Agent to send with the request",
                        default='')
    parser.add_argument('-hf', '--headersfile', type=str, default=None,
                        help="Parameter that passes an HTTP request"
                             + " header file to be scanned.")

    parser.add_argument('-S', '--spider', action='store_true',
                        help='flag to run spider', required=False)

    parser.add_argument('-w', '--workers', type=int, default=4,
                        help="Defines the number of workers.")
    parser.add_argument('--domain', type=str, default=None,
                        help="Defines the domain of the web crawler.")
    args = vars(parser.parse_args())

    if not any(args.values()):
        parser.error('No arguments provided.')
        sys.exit(0)
    if args['spider'] and not args['geturls']:
        parser.error('--spider can only be used with --geturls')
        sys.exit(0)
    if args['agent'] and args['cookie'] and args['headersfile']:
        parser.error("The arguments --cookie, --agent --headers file cannot be used together.")
        sys.exit(0)
    if args['agent'] and args['headersfile']:
        parser.error("The arguments --agent, --headers file cannot be used together.")
        sys.exit(0)
    if args['cookie'] and args['headersfile']:
        parser.error("The arguments --cookie, --headers file cannot be used together.")
        sys.exit(0)
    sp = TreatArguments(args)
    sp.run()


if __name__ == '__main__':
    main()
