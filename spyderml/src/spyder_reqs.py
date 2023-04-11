import datetime
import hashlib
import json
import os
import tempfile
import unicodedata

import requests
from colorama import Fore, Style

from spyderml import __version__


class Cacherequest:

    def __init__(self, cache=True, life=1, proxy=None, headers=None):
        self.cache = cache
        self.life = life
        self.version = __version__.replace(".", "")
        self.text = None
        self.headers_text = []
        self.proxy = proxy
        self.headers = headers
        self.session = requests.Session()

    def get(self, url):
        path_to_cache_file = os.path.join(tempfile.gettempdir(), "get" +
                                          hashlib.md5(url.encode()).hexdigest() + self.version)
        if self.cache:
            if os.path.exists(path_to_cache_file):
                buffer = json.loads(open(path_to_cache_file, 'r').read())
                if datetime.datetime.utcnow() < datetime.datetime.strptime(buffer["data"], "%Y-%m-%d %H:%M:%S"):
                    self.text = buffer["html"]
                    return True

        try:
            if self.headers is not None:
                if self.proxy is not None:
                    self.session.proxies.update(self.proxy)
                page = self.session.get(url=url, headers=self.headers, allow_redirects=True)
            else:
                if self.proxy is not None:
                    self.session.proxies.update(self.proxy)
                page = self.session.get(url)
            page.encoding = "utf-8"
            self.text = unicodedata.normalize(u'NFKD', page.text).encode('ascii', 'ignore').decode("utf-8")
            if self.cache:
                with open(path_to_cache_file, '+w') as file:
                    file.write(json.dumps({"data": (datetime.datetime.utcnow()
                                                    + datetime.timedelta(minutes=self.life)).strftime(
                        "%Y-%m-%d %H:%M:%S"),
                        "html": self.text}))
        except requests.exceptions.SSLError:
            print(f"{Fore.RED}{url}\t<SSL Error>{Style.RESET_ALL}")
            exit()
        except requests.exceptions.MissingSchema:
            print(f"{Fore.RED}{url}:\nInvalid url\n http://?{Style.RESET_ALL}")
            exit()
        except requests.exceptions.InvalidSchema:
            print(f"{Fore.RED}{url} ERROR{Style.RESET_ALL}")
            exit()
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}Attempt to connect to the host: {url} refused...\n"
                  f"Tip: Try to exchange https for http or http for https.{Style.RESET_ALL}")
            exit()

    def post(self, url, data):
        path_to_cache_file = os.path.join(tempfile.gettempdir(), "post" +
                                          hashlib.md5(url.encode()).hexdigest() + self.version)
        if self.cache:
            if os.path.exists(path_to_cache_file):
                buffer = json.loads(open(path_to_cache_file, 'r').read())
                if datetime.datetime.utcnow() < datetime.datetime.strptime(buffer["data"], "%Y-%m-%d %H:%M:%S"):
                    self.text = buffer["html"]
                    return True
        try:
            if self.headers is not None:
                if self.proxy is not None:
                    self.session.proxies.update(self.proxy)
                if data is not None:
                    page = self.session.post(url=url, headers=self.headers, data=data, allow_redirects=True)
                else:
                    page = self.session.post(url=url, headers=self.headers, allow_redirects=True)
            else:
                if self.proxy is not None:
                    self.session.proxies.update(self.proxy)
                if data:
                    page = self.session.post(url, data=data, allow_redirects=True)
                else:
                    page = self.session.post(url, allow_redirects=True)
            page.encoding = "utf-8"
            self.text = unicodedata.normalize(u'NFKD', page.text).encode('ascii', 'ignore').decode("utf-8")
            if self.cache:
                with open(path_to_cache_file, '+w') as file:
                    file.write(json.dumps({"data": (datetime.datetime.utcnow()
                                                    + datetime.timedelta(minutes=self.life)).strftime(
                        "%Y-%m-%d %H:%M:%S"),
                        "html": self.text}))
        except requests.exceptions.SSLError:
            print(f"{Fore.RED}{url}\t<SSL Error>{Style.RESET_ALL}")
            exit()
        except requests.exceptions.MissingSchema:
            print(f"{Fore.RED}{url}:\nInvalid url\n http://?{Style.RESET_ALL}")
            exit()
        except requests.exceptions.InvalidSchema:
            print(f"{Fore.RED}{url} ERROR{Style.RESET_ALL}")
            exit()
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}Attempt to connect to the host: {url} refused...\n"
                  f"Tip: Try to exchange https for http or http for https.{Style.RESET_ALL}")
            exit()

    def response_and_request_headers(self, url):
        try:
            if self.proxy is not None:
                self.session.proxies.update(self.proxy)
            r_headers = self.session.get(url)
            request_headers = r_headers.request.headers
            self.headers_text.append(request_headers)
            self.headers_text.append(r_headers.headers)
        except requests.exceptions.SSLError:
            print(f"{Fore.RED}{url}\t<SSL Error>{Style.RESET_ALL}")
            exit()
        except requests.exceptions.MissingSchema:
            print(f"{Fore.RED}{url}:\nInvalid url\n http://?{Style.RESET_ALL}")
            exit()
        except requests.exceptions.InvalidSchema:
            print(f"{Fore.RED}{url} ERROR{Style.RESET_ALL}")
            exit()
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}Attempt to connect to the host: {url} refused...\n"
                  f"Tip: Try to exchange https for http or http for https.{Style.RESET_ALL}")
            exit()
