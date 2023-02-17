from urllib.parse import urljoin

import requests
import urllib3
import logging
import webtech

from bs4 import BeautifulSoup as Bs
from bs4 import Comment
from colorama import Fore, Style

from spyderml.lib import cache_manipulator
from spyderml.lib.file import save_output


def treat_objects(objects: str):
    if "," in objects:
        objects = objects.split(',')
        return objects
    return objects


def update_database():
    webtech.database.update_database(force=True)


def detect_technologies(url, filepath=None):
    webtech.database.update_database()
    # you can use options, same as from the command line
    wt = webtech.WebTech(options={'json': True})

    # scan a single website
    try:
        report = wt.start_from_url(url)
        techs = report['tech']
        if filepath is not None:
            save_output(filename=filepath, text=f"\nSite: {url} technologies:")
        print("Site: {} technologies:".format(url))

        for tech in techs:
            if filepath is not None:
                save_output(filename=filepath, text=f"Name: {tech['name']}\tVersion: {tech['version']}")
            print(f'''{tech['version']}
            ''')
        print('\n')
    except webtech.utils.ConnectionException:
        print("Connection error")


def spyder_request(target, useragent=None, cookie=None, headersfile=None):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    cache = cache_manipulator.Cacherequest(life=60)
    try:
        if useragent is not None or cookie is not None:
            if useragent and cookie:
                headers = {
                    "User-Agent": useragent,
                    "Cookie": cookie
                }
            elif cookie:
                headers = {
                    'Cookie': cookie
                }
            else:
                headers = {
                    'User-Agent': useragent
                }
            html = requests.get(url=target, headers=headers, allow_redirects=True)
            return html.text
        elif headersfile is not None:
            html = requests.get(url=target, headers=headersfile, allow_redirects=True)
            return html.text

        cache.get(target)
        return cache.text
    except requests.exceptions.SSLError:
        print(f"{Fore.RED}{target}\t<SSL Error>{Style.RESET_ALL}")
        exit()
    except requests.exceptions.MissingSchema:
        print(f"{Fore.RED}{target}:\nInvalid url\n http://?{Style.RESET_ALL}")
        exit()
    except requests.exceptions.InvalidSchema:
        print(f"{Fore.RED}{target} ERROR{Style.RESET_ALL}")
        exit()
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Attempt to connect to the host: {target} refused...\n"
              f"Tip: Try to exchange https for http or http for https.{Style.RESET_ALL}")
        exit()
    except Exception as e:
        logging.critical(e)
        exit()


def soup_tags(document, object, file=None):
    html = Bs(document, 'html.parser')
    results = html.find_all(object)
    for result in results:
        if file is not None:
            save_output(filename=file, text=result)
        print(result)


def soup_comments(document, file=None):
    html = Bs(document, 'html.parser')
    comments = html.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if file is not None:
            save_output(filename=file, text=comment)
        print(comment)


def soup_attrs(document, object, file=None):
    html = Bs(document, 'html.parser')
    if type(object) == list:
        for o in object:
            for attribute in html.select(f"[{o}]"):
                if file is not None:
                    save_output(filename=file, text=attribute)
                print(attribute)
    else:
        for attribute in html.select(f"[{object}]"):
            if file is not None:
                save_output(filename=file, text=attribute)
            print(attribute)


def get_js(url, document, file=None):
    html = Bs(document, 'html.parser')
    for script in html.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(url, script.attrs.get("src"))
            if file is not None:
                save_output(filename=file, text=script_url)
            print(script_url)





def print_html(document, file=None):
    if file is not None:
        save_output(filename=file, text=document)
    print(document)
