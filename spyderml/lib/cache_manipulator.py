import tempfile
import os
import requests
import unicodedata
import hashlib
import json
import datetime

from spyderml import __version__


class Cacherequest:

    def __init__(self, cache=True, life=1):
        self.cache = cache
        self.life = life
        self.version = __version__.replace(".", "")
        self.text = None

    def get(self, url):
        path_to_cache_file = os.path.join(tempfile.gettempdir(),
                                          hashlib.md5(url.encode()).hexdigest() + self.version)
        if self.cache:
            if os.path.exists(path_to_cache_file):
                buffer = json.loads(open(path_to_cache_file, 'r').read())
                if datetime.datetime.utcnow() < datetime.datetime.strptime(buffer["data"], "%Y-%m-%d %H:%M:%S"):
                    self.text = buffer["html"]
                    return True

        page = requests.get(url)
        page.encoding = "utf-8"
        self.text = unicodedata.normalize(u'NFKD', page.text).encode('ascii', 'ignore').decode("utf-8")
        if self.cache:
            with open(path_to_cache_file, '+w') as file:
                file.write(json.dumps({"data": (datetime.datetime.utcnow()
                                                + datetime.timedelta(minutes=self.life)).strftime(
                    "%Y-%m-%d %H:%M:%S"),
                                       "html": self.text}))


