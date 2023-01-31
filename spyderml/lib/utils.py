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


def spyder_request(target):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    cache = cache_manipulator.Cacherequest(life=60)
    try:
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
    else:
        return r


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


def get_all_urls(document, file=None):
    soup = Bs(document, 'html.parser')
    urls = set([a['href'] for a in soup.find_all('a', href=True)])
    print(f"{Fore.BLUE}[*]{Style.RESET_ALL} URLs encontradas: {len(urls)}")
    for url in urls:
        try:
            response = requests.get(url=url, timeout=10, allow_redirects=True)
            if file is not None:
                save_output(filename=file, text=url)
            elif 200 <= response.status_code < 300:
                print(
                    f"\t{Fore.BLUE}[+]{Style.RESET_ALL} {url} <{Fore.GREEN}{response.status_code}{Style.RESET_ALL}>" +
                    f"\tSize: <{len(response.content)}>")
            elif 300 <= response.status_code < 400:
                print(
                    f"\t{Fore.YELLOW}[!]{Style.RESET_ALL} {url} <{Fore.YELLOW}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            elif 400 <= response.status_code < 500:
                print(
                    f"\t{Fore.RED}[-]{Style.RESET_ALL} {url} <{Fore.RED}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            elif 500 <= response.status_code <= 504:
                print(
                    f"\t{Fore.YELLOW}[!]{Style.RESET_ALL} {url} <{Fore.CYAN}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            else:
                print(
                    f"\t{Fore.YELLOW}[?]{Style.RESET_ALL} {url}<{response.status_code}>"
                    + f"\tSize: <{len(response.content)}>")

        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.SSLError:
            print(f"\t{Fore.RED}[-]{Style.RESET_ALL} {url} <{Fore.RED}SSL Error{Style.RESET_ALL}>")
        except requests.exceptions.ConnectTimeout:
            print(f"\t{Fore.RED}[-]{Style.RESET_ALL} {url} <{Fore.RED}Timeout{Style.RESET_ALL}>")
        except Exception as e:
            if "javascript:void(0)" in str(response.content):
                continue
            else:
                print(f"\n\t{Fore.RED}ERROR:{Style.RESET_ALL} {url} <{Fore.RED}{e}{Style.RESET_ALL}>\n")

def print_html(document, file = None):
    if file is not None:
        save_output(filename = file, text=document)
    print(document)