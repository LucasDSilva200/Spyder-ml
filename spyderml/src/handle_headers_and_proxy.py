from spyderml.src.file import open_headers_file


def handle_headers(useragent, cookies, headersfile):
    if useragent is not None or cookies is not None:
        if useragent and cookies:
            headers = {
                "User-Agent": useragent,
                "Cookie": "; ".join(cookies)
            }
        elif cookies:
            headers = {
                'Cookie': "; ".join(cookies)
            }
        else:
            headers = {
                'User-Agent': useragent
            }

    elif headersfile is not None:
        headers = open_headers_file(headers_file=headersfile)
    else:
        headers = None

    return headers


def handle_proxy(proxy):
    if proxy == 'burpsuite':
        proxies = {
            'http': 'http://localhost:8080',
            'https': 'http://localhost:8080'
        }
    elif proxy is None:
        return proxy
    elif proxy == 'tor':
        proxies = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }
    else:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    return proxies


def handle_data(data):
    if data:
        data_dict = {}
        for item in data:
            key, value = item.split(':')
            data_dict[key] = value
    else:
        data_dict = None
    return data_dict
