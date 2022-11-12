import requests
import urllib3

from bs4 import BeautifulSoup as bs
from bs4 import Comment

from spyderml.lib.file import save_output


def treat_objects(objects: str):
    if "," in objects:
        objetos = objects.split(',')
        return objects
    return objects


def spyder_request(target):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        r = requests.get(target)
        return r
    except requests.exceptions.SSLError:
        print(f"{target}:\nErro de ssl")
        exit()
    except requests.exceptions.MissingSchema:
        print(f"{target}:\nInvalid url\n http://?")
        exit()
    except requests.exceptions.InvalidSchema:
        print(f"{target} ERROR")
        exit()
    except:
        print("UNKNOWN ERROR")
        exit()


def soup_tags(document, object, file=None):
    html = bs(document.content, 'html.parser')
    results = html.find_all(object)
    for result in results:
        if file is not None:
            save_output(filename=file, text=result)
        print(result)


def soup_comments(document, file=None):
    html = bs(document.content, 'html.parser')
    comments = html.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if file is not None:
            save_output(filename=file, text=comment)
        print(comment)


def soup_attrs(document, object, file=None):
    html = bs(document.content, 'html.parser')
    if type(object) == list:
        for o in object:
            print(o)
            for attribute in html.select(f"[{o}]"):
                if file is not None:
                    save_output(filename=file, text=attribute)
                print(attribute)
    else:
        for attribute in html.select(f"[{object}]"):
            if file is not None:
                save_output(filename=file, text=attribute)
            print(attribute)
