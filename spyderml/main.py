#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import argcomplete

from spyderml.src import spyder_reqs
from spyderml.src.asciiarts import banner
from spyderml.src.handle_headers_and_proxy import handle_headers,\
    handle_proxy, handle_data
from spyderml.src.spidercrawler import get_all_urls, WebCrawling
from spyderml.src.utils import treat_objects, soup_tags,\
    soup_comments, soup_attrs, get_js, \
    detect_technologies, update_database, print_html,\
    json_response, print_headers

'''
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
'''

# Classe que trata os argumentos passados pela função main()


class TreatArguments:
    def __init__(self, args):
        self.args = args

    # Método que trata e define a ação que será tratada pela aplicação
    def run(self):
        print(banner())
        headers = handle_headers(useragent=self.args['agent'],
                                 cookies=self.args['cookie'],
                                 headersfile=self.args['headersfile'])
        proxy = handle_proxy(self.args['proxy'])
        data = handle_data(self.args['data'])
        try:
            if self.args['update']:
                update_database()

            else:
                if headers is not None:
                    spyder_request = spyder_reqs.Cacherequest(life=60,
                                                              cache=self.args[
                                                                  'cache'],
                                                              proxy=proxy,
                                                              headers=headers)
                    if self.args['tr'].lower() == 'post':
                        spyder_request.post(url=self.args['target'], data=data)
                    elif self.args['tr'].lower() == 'get':
                        spyder_request.get(url=self.args['target'])
                    html_document = spyder_request.text
                else:
                    spyder_request = spyder_reqs.Cacherequest(life=60,
                                                              cache=self.args[
                                                                  'cache'],
                                                              proxy=proxy)
                    if self.args['tr'].lower() == 'post':
                        spyder_request.post(url=self.args['target'], data=data)
                    elif self.args['tr'].lower() == 'get':
                        spyder_request.get(url=self.args['target'])
                    html_document = spyder_request.text

                if self.args['tags']:
                    tags = treat_objects(objects=self.args['tags'])
                    soup_tags(document=html_document, object=tags,
                              file=self.args['output'])
                elif self.args['comments']:
                    soup_comments(document=html_document,
                                  file=self.args['output'])
                elif self.args['getjs']:
                    get_js(
                        url=self.args['target'], document=html_document,
                        file=self.args['output'])
                elif self.args['techs']:
                    detect_technologies(
                        url=self.args['target'], filepath=self.args['output'])
                elif self.args['geturls']:
                    if self.args['spider']:
                        wc = WebCrawling(permission=self.args['spider'],
                                         workers=self.args['workers'],
                                         filepath=self.args['output'],
                                         domain=self.args['domain'])
                        wc.pre_queue_to_crawling(url=self.args['target'])
                    else:
                        get_all_urls(document=html_document,
                                     file=self.args['output'])
                elif self.args['html']:
                    print_html(document=html_document,
                               file=self.args['output'])
                elif self.args['jsr']:
                    json_response(document=html_document,
                                  file=self.args['output'])

                elif self.args['attribs']:
                    attr = treat_objects(objects=self.args['attribs'])
                    soup_attrs(document=html_document, object=attr,
                               file=self.args['output'])
                else:
                    spyder_request.response_and_request_headers(
                        url=self.args['target'])
                    print_headers(spyder_request.headers_text,
                                  filenane=self.args['output'])
        except KeyboardInterrupt:
            print("\nClossing...\n")
            sys.exit(0)


# Passando os argumentos de linha de comando com o argparse
def main():
    parser = argparse.ArgumentParser(
        description="A tool made to facilitate the analysis of html code.")

    group_target = parser.add_mutually_exclusive_group()

    group_action = parser.add_mutually_exclusive_group()

    group_target.add_argument('-t', '--target', type=str, help="Parameter that"
                              + " defines the target URL "
                              + "http://example.com/index.html")
    parser.add_argument('--tr', type=str, default="GET",
                        help='Type of request.')
    group_target.add_argument('--update', help='Flag responsible for '
                              + 'updating the database.',
                              default=False, action='store_true')
    group_action.add_argument(
        '--tags', type=str, help="Flag that defines which tags the"
        + " program will bring")

    group_action.add_argument(
        '--comments', help="Flag that brings the comments",
        default=False, action='store_true', )

    group_action.add_argument('--attribs', type=str,
                              help="Flag that defines which "
                              + "attributes the application will look for.")

    group_action.add_argument('--getjs', help='Flag that brings all JS files '
                              + 'from the page.',
                              default=False, action='store_true')
    group_action.add_argument('--techs', help='Flag trying to discover '
                              + 'the technologies of the page.',
                              default=False, action='store_true')
    group_action.add_argument('--geturls', help='This flag takes all '
                              + 'the target\'s urls and tries to access them.',
                              default=False, action='store_true')

    group_action.add_argument('--html', help='This Flag results in '
                              + 'all the page\'s html code.',
                              default=False, action='store_true')
    group_action.add_argument('--jsr', action='store_true', default=False,
                              help="Makes a request that returns a JSON.")
    parser.add_argument('-o', '--output', type=str,
                        help="Flag that defines in which file "
                        + "the command output will be "
                             "saved.")
    parser.add_argument('-C', '--cookie', type=str, help="Cookie to send "
                        + "with the request",
                        default=None)
    parser.add_argument('-A', '--agent', type=str, help="User-Agent to send "
                        + "with the request",
                        default=None)
    parser.add_argument('-hf', '--headersfile', type=str, default=None,
                        help="Parameter that passes an HTTP request"
                             + " header file to be scanned.")

    parser.add_argument('-S', '--spider', action='store_true',
                        help='flag to run spider', default=False)

    parser.add_argument('-w', '--workers', type=int, default=4,
                        help="Defines the number of workers.")
    parser.add_argument('--domain', type=str, default=None,
                        help="Defines the domain of the web crawler.")
    parser.add_argument('--cache', action='store_true', default=False,
                        help="Defines whether to create cache or "
                        + "not (default: false).")
    parser.add_argument('--proxy', type=str, default=None,
                        help="Defines the proxy that will be used "
                        + "(Which can be passed tor or burpsuite to use these"
                             + " two default proxies).")
    parser.add_argument('-D', '--data', nargs='+',
                        help="Data to send with the request in format "
                        + "key1:value1 key2:value2 key3:value3...")

    argcomplete.autocomplete(parser)

    args = vars(parser.parse_args())

    if not any(args.values()):
        parser.error('No arguments provided.')
        sys.exit(0)
    if not args['target'] and not args['update']:
        parser.error('No url the file with defined urls.')
        sys.exit(0)
    if args['spider'] and not args['geturls']:
        parser.error('--spider can only be used with --geturls')
        sys.exit(0)
    if args['agent'] and args['cookie'] and args['headersfile']:
        parser.error(
            "The arguments --cookie, --agent --headers "
            + "file cannot be used together.")
        sys.exit(0)
    if args['agent'] and args['headersfile']:
        parser.error(
            "The arguments --agent, --headers file cannot be used together.")
        sys.exit(0)
    if args['cookie'] and args['headersfile']:
        parser.error(
            "The arguments --cookie, --headers file cannot be used together.")
        sys.exit(0)
    sp = TreatArguments(args)
    sp.run()


if __name__ == '__main__':
    main()
