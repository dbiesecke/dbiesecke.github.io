"""
dubsstreamz.com

method:
first iframe
var rSI : string = ""
var tlc : [string]
var mn : int
for each s in tlc:
    b64 = base64.b64decode(s).decode("utf-8")
    str = re.sub('\D', '', b64)
    str_n = int(str)
    str_n -= 61751400
    rSI += chr(str_n)
return rSI
"""

NAME = "dubsstreamz.com"
KEY = "dubsstreamzcom"
BASE = "www.dubsstreamz.com"

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
    p_url = parse_url(url)
    html = http_get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    f_iframe_url = soup.find("iframe").get("src")
    headers.update({"Referer": url})
    html = http_get(f_iframe_url, headers=headers)
    rSI = algo(html.text)
    return [rSI]

def algo(text):
    regex = r" = \[(.*)\]"
    rSI = ""
    tlc = re.search(regex, text, re.MULTILINE | re.DOTALL).group(1)
    tlc = re.sub('\s', '', tlc)
    tlc = tlc.split(",")
    tlc = list(map(lambda x: x.strip('"'), tlc))
    mn = re.search(r"\)\) - (\d+)\);", text).group(1).strip()
    mn = int(mn)
    for s in tlc:
        b64 = base64.b64decode(s).decode("utf-8")
        str = re.sub('\D', '', b64)
        if (str):
            str_n = int(str)
            str_n -= mn
            rSI += chr(str_n)
    return re.search(r"source = '(.*?)'", rSI).group(1)
    

if __name__ == "__main__":
    def test(url):
        vid_urls = get_urls(url)
        print(vid_urls)

    def test_can_handle(url):
        print(can_handle(url))

    test("http://www.dubsstreamz.com/watch/sports/live/everton-vs-crystal-palace.html")
    test_can_handle("http://www.dubsstreamz.com/watch/sports/live/everton-vs-crystal-palace.html")
