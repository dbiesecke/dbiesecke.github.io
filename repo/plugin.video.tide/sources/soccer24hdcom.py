"""
soccer24hd.com

method:
first iframe -> first iframe -> first iframe
search for window.atob
decode base64
"""

NAME = "soccer24hd.com"
KEY = "soccer24hdcom"
BASE = "soccer24hd.com"

if __name__ == "__main__":
    import sys
    import os
    import json
    # ugly hack, but oh well
    sys.path.append("%s/.kodi/addons/plugin.video.tide" % os.getenv("HOME"))

try:
    from router import PLUGIN, path_for_source
    from helpers import http_get, header_random_agent, log
    from common import add_headers, add_items, parse_url
except Exception as e:
    print(e)

import urllib
import base64
import re
from bs4 import BeautifulSoup 

def can_handle(url):
    p_url = parse_url(url)
    return p_url.netloc == BASE

@PLUGIN.route("%s/<url>" % path_for_source(KEY))
def root(url):
    ref_url = urllib.unquote(url).decode('utf8')
    urls = get_urls(ref_url)
    add_items(urls, ref_url, PLUGIN)

def get_urls(url):
    headers = header_random_agent()
    cookies = {}
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    f_iframe_1_url = soup.find("iframe").get("src")
    headers.update({"Referer": url})
    html = http_get(f_iframe_1_url, headers=headers, cookies=cookies)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    f_iframe_2_url = soup.find("iframe").get("src")
    html = http_get(f_iframe_2_url, headers=headers)
    cookies.update(html.cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    f_iframe_3_url = soup.find("iframe").get("src")
    headers.update({"Referer": f_iframe_3_url})
    html = http_get(f_iframe_3_url, headers=headers)
    b64_str = re.search(r"window\.atob\(\"(.*)\"\)", html.text).group(1)
    de_str = base64.b64decode(b64_str).decode("utf-8") 
    return [de_str]

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("https://soccer24hd.com/game/match/1189/Sampdoria-Vs-Napoli.html")
    test_can_handle("https://soccer24hd.com/game/match/1189/Sampdoria-Vs-Napoli.html")
