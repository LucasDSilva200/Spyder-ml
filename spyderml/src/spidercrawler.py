import sys
import threading
import queue
import requests

from bs4 import XMLParsedAsHTMLWarning, BeautifulSoup as Bs
from colorama import Fore, Style
from spyderml.src.file import save_output


def request(url):
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        html = response.text
        return html
    except requests.exceptions.MissingSchema:
        pass
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.InvalidSchema:
        pass
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.SSLError:
        pass
    except requests.exceptions.ConnectionError:
        pass


def get_all_urls(document, file=None):
    soup = Bs(document, 'html.parser')
    urls = set([a['href'] for a in soup.find_all('a', href=True)])
    print(f"{Fore.BLUE}[*]{Style.RESET_ALL} URLs encontradas: {len(urls)}")
    for url in urls:
        try:
            response = requests.get(url=url, timeout=10, allow_redirects=True)
            if 200 <= response.status_code < 300:
                print(
                    f"\t{Fore.BLUE}[+]{Style.RESET_ALL} {url} "
                    + f"<{Fore.GREEN}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            elif 300 <= response.status_code < 400:
                print(
                    f"\t{Fore.YELLOW}[!]{Style.RESET_ALL} {url} "
                    + f"<{Fore.YELLOW}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            elif 400 <= response.status_code < 500:
                print(
                    f"\t{Fore.RED}[-]{Style.RESET_ALL} {url} "
                    + f"<{Fore.RED}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            elif 500 <= response.status_code <= 504:
                print(
                    f"\t{Fore.YELLOW}[!]{Style.RESET_ALL} {url} "
                    + f"<{Fore.CYAN}{response.status_code}{Style.RESET_ALL}>"
                    + f"\tSize: <{len(response.content)}>")
            else:
                print(
                    f"\t{Fore.YELLOW}[?]{Style.RESET_ALL} {url}"
                    + f"<{response.status_code}>"
                    + f"\tSize: <{len(response.content)}>")

        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.SSLError:
            print(
                f"\t{Fore.RED}[-]{Style.RESET_ALL} {url} "
                + f"<{Fore.RED}SSL Error{Style.RESET_ALL}>")
        except requests.exceptions.ConnectTimeout:
            print(
                f"\t{Fore.RED}[-]{Style.RESET_ALL} {url} "
                + f"<{Fore.RED}Timeout{Style.RESET_ALL}>")
        except Exception as e:
            if "javascript:void(0)" in str(response.content):
                continue
            else:
                print(
                    f"\n\t{Fore.RED}ERROR:{Style.RESET_ALL} {url} "
                    + f"<{Fore.RED}{e}{Style.RESET_ALL}>\n")

        else:
            if file is not None:
                save_output(filename=file, text=url)


def get_links(html, domain):
    try:
        links = []
        soup = Bs(html, 'html.parser')
        tags_a = soup.find_all('a', href=True)
        for tag in tags_a:
            link = tag["href"]
            if link.startswith("http"):
                if domain is not None:
                    if domain in link:
                        links.append(link)
                else:
                    links.append(link)
        return links
    except TypeError:
        pass
    except KeyError:
        pass
    except XMLParsedAsHTMLWarning:
        pass
    except Exception as e:
        print(f"ERROR: {e}")


# Classe webcrawling que gerencia as threads e a fila do crawler
class WebCrawling:
    def __init__(self, permission, filepath=None, domain=None, workers=4):
        self.permission = permission
        self.to_crawl = queue.Queue()
        self.crawled = set()
        self.domain = domain
        self.workers = workers
        self.filepath = filepath

    def send_request(self):
        while True:
            try:
                url = self.to_crawl.get_nowait()
            except queue.Empty:
                break
            try:
                html = request(url=url)
                links = get_links(html=html, domain=self.domain)
                if links:
                    for link in links:
                        if link not in self.crawled and \
                                link not in self.to_crawl.queue:
                            self.to_crawl.put(link)

                if self.filepath is not None:
                    save_output(filename=self.filepath, text=url)
                print(f"[{Fore.BLUE}+{Style.RESET_ALL}] {url}")
            except KeyboardInterrupt:
                print("\nClossing....\n")
                sys.exit(0)

            finally:
                self.crawled.add(url)

    def pre_queue_to_crawling(self, url):
        num_threads = self.workers
        threads = []
        self.to_crawl.put(url)
        for i in range(num_threads):
            t = threading.Thread(target=self.send_request())
            threads.append(t)
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()
