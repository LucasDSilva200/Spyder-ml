from urllib.parse import urljoin

import requests
import urllib3
import logging
import webtech

from bs4 import BeautifulSoup as Bs
from bs4 import Comment

from spyderml.lib.file import save_output


def treat_objects(objects: str):
    if "," in objects:
        objects = objects.split(',')
        return objects
    return objects


def update_database():
    webtech.database.update_database(force=True)


def detect_technologies(url):
    webtech.database.update_database()
    # you can use options, same as from the command line
    wt = webtech.WebTech(options={'json': True})

    # scan a single website
    try:
        report = wt.start_from_url(url)
        techs = report['tech']
        print("Site: {} technologies:".format(url))

        for tech in techs:
            print(f"Name: {tech['name']}\tVersion: {tech['version']}")
        print('\n')
    except webtech.utils.ConnectionException:
        print("Connection error")


def spyder_request(target):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        r = requests.get(target)
    except requests.exceptions.SSLError:
        print(f"{target}:\nSSL Error")
        exit()
    except requests.exceptions.MissingSchema:
        print(f"{target}:\nInvalid url\n http://?")
        exit()
    except requests.exceptions.InvalidSchema:
        print(f"{target} ERROR")
        exit()
    except requests.exceptions.ConnectionError:
        print(f"Attempt to connect to the host: {target} refused...\n"
              "Tip: Try to exchange https for http or http for https.")
        exit()
    except Exception as e:
        logging.critical(e)
        exit()
    else:
        return r


def soup_tags(document, object, file=None):
    html = Bs(document.content, 'html.parser')
    results = html.find_all(object)
    for result in results:
        if file is not None:
            save_output(filename=file, text=result)
        print(result)


def soup_comments(document, file=None):
    html = Bs(document.content, 'html.parser')
    comments = html.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if file is not None:
            save_output(filename=file, text=comment)
        print(comment)


def soup_attrs(document, object, file=None):
    html = Bs(document.content, 'html.parser')
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
    html = Bs(document.content, 'html.parser')
    for script in html.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(url, script.attrs.get("src"))
            if file is not None:
                save_output(filename=file, text=script_url)
            print(script_url)
