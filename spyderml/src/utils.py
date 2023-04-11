import json
from urllib.parse import urljoin

import webtech
from bs4 import BeautifulSoup as Bs
from bs4 import Comment
from colorama import Fore, Style

from spyderml.src.file import save_output


def treat_objects(objects):
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
                save_output(
                    filename=filepath, text=f"Name: {tech['name']}\tVersion: "
                    + f"{tech['version']}")
            print(f'''{tech['version']}
            ''')
        print('\n')
    except webtech.utils.ConnectionException:
        print("Connection error")


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


def json_response(document, file=None):
    json_content = json.loads(document)
    if file is not None:
        save_output(filename=file, text=json_content)
    print(json.dumps(json_content, indent=4))


def print_headers(headers_dict_list, filenane=None):
    if filenane is not None:
        for index, headers_dict in enumerate(headers_dict_list):
            if index == 0:
                save_output(filename=filenane,
                            text="------------Request Headers-----------")
            elif index == 1:
                save_output(filename=filenane,
                            text="------------Response Headers-----------")
            for key in headers_dict:
                save_output(filename=filenane,
                            text=f"{key}: {headers_dict[key]}")
            save_output(filename=filenane, text="-"*39+"\n")
    for index, headers_dict in enumerate(headers_dict_list):
        if index == 0:
            print(
                f"------------{Fore.CYAN}Request Headers{Style.RESET_ALL}"
                + "-----------")
        elif index == 1:
            print(
                f"------------{Fore.CYAN}Response Headers{Style.RESET_ALL}"
                + "-----------")
        for key in headers_dict.keys():
            print(
                f"{Fore.LIGHTMAGENTA_EX}{key}{Style.RESET_ALL}: "
                + f"{headers_dict[key]}")

        print("-"*39+"\n")
