"""
techobest.com

method:
generic m3u8 searcher
"""

NAME = "techobest.com"
KEY = "techobestcom"
BASE = "techobest.com"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    import generic_m3u8_searcher
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from common import add_items, parse_url
except Exception as e:
    print(e)

import random
import requests
import time
import re
import base64
import urllib

def can_handle(url):
    p_url = parse_url(url)
    return p_url.netloc == BASE

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_sucuri_cookie(result):
    try:
        s = re.compile("S\s*=\s*'([^']+)").findall(result)[0]
        s = base64.b64decode(s).decode("ascii")
        s = re.sub(' ', '', s)
        s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
        s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
        s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
        s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
        s = re.sub(';location.reload\(\);', '', s)
        s = re.sub(r'\n', '', s)
        s = re.sub(r'document\.cookie', 'cookie', s)
        parts = s.split(";", 1)
        sseiw = parts[0]
        cbdfbd = parts[1]
        cbdfbd = re.sub('cookie=', '', cbdfbd)
        exec(sseiw)
        cookie = eval(cbdfbd)
        parts = cookie.split(";")
        name_val = parts[0].split("=")
        path_val = parts[1].split("=")
        maxage_val = parts[2].split("=")

        return {
            "name": name_val[0],
            "value": name_val[1],
            "path": path_val[1],
            "max-age": maxage_val[1],
        }
    except Exception as e:
        return None

def get_urls(url):
    header = header_random_agent()
    cookie = None
    for i in range(5):
        html = http_get(url, headers=header)
        cookie = get_sucuri_cookie(html.text)
        if cookie != None:
            break
        time.sleep(random.uniform(2,0.5))
    if cookie == None:
        return []
    cookies_jar = requests.cookies.RequestsCookieJar()
    cookies_jar.set(cookie["name"], cookie["value"], path=cookie["path"])
    html = http_get(url, headers=header, cookies = cookies_jar)
    urls = generic_m3u8_searcher.search(html.text)
    return urls

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://techobest.com/soccer5?utm_source=soccer100")
    test_can_handle("http://techobest.com/soccer5?utm_source=soccer100")
