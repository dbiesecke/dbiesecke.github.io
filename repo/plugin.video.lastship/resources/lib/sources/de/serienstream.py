# -*- coding: UTF-8 -*-

"""
    Lastship Add-on (C) 2019
    Credits to Lastship, Placenta and Covenant; our thanks go to their creators

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Addon Name: Lastship
# Addon id: plugin.video.lastship
# Addon Provider: Lastship

import json
import re
import urllib
import urlparse
import difflib
import random

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import duckduckgo
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
from resources.lib.modules import source_faultlog


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['s.to']
        self.base_link = 'https://s.to'
        self.search_link = '/serien'
        
        u1 = control.setting('serienstream.user')
        p1 = control.setting('serienstream.pass')
        u2 = control.setting('serienstream.user2')
        p2 = control.setting('serienstream.pass2')
        u3 = control.setting('serienstream.user3')
        p3 = control.setting('serienstream.pass3')
        u4 = control.setting('serienstream.user4')
        p4 = control.setting('serienstream.pass4')
        u5 = control.setting('serienstream.user5')
        p5 = control.setting('serienstream.pass5')
        
        data = []
        for i in xrange(1, 6):
            u = vars()['u' + str(i)]
            p = vars()['p' + str(i)]
            if u and p:
                data.append((u,p))
        
        saccount = random.sample(data, 1)
        
        self.login = saccount[0][0]
        self.password = saccount[0][1]
            
        self.cookie = ''
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

    def movie(self, imdb, title, localtitle, aliases, year):
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:

            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url: url = duckduckgo.search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year, self.base_link, ">(.*)")
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url[:-1] if url.endswith('/') else url
            if "staffel" in url:
                url = re.findall("(.*?)staffel", url)[0]
            url += '/staffel-%d/episode-%d/' % (int(season), int(episode))
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = cache.get(client.request, 4, urlparse.urljoin(self.base_link, url))

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'hosterSiteVideo'})
            r = dom_parser.parse_dom(r, 'li', attrs={'data-lang-key': re.compile('[1|2|3]')})
            r = [(i.attrs['data-link-target'], dom_parser.parse_dom(i, 'h4'),
                  'subbed' if i.attrs['data-lang-key'] == '3' else '' if i.attrs['data-lang-key'] == '1' else 'subbed' if i.attrs['data-lang-key'] == '2' else '') for i
                 in r]
            r = [(i[0], re.sub('\s(.*)', '', i[1][0].content), 'HD' if 'hd' in i[1][0][1].lower() else 'SD', i[2]) for i in r]

            for link, host, quality, info in r:
                print host
                #if 'HD' in quality: host = re.findall('(.+?)\s*<br', host)[0]
                valid, host = source_utils.is_host_valid(host, hostDict)
                if not valid: continue

                sources.append(
                    {'source': host, 'quality': quality, 'language': 'de', 'url': link, 'info': info, 'direct': False,
                     'debridonly': False})

            return sources
        except:
            source_faultlog.logFault(__name__, source_faultlog.tagScrape, url)
            return sources

    def resolve(self, url):
        try:
            url = cache.get(client.request, 4, urlparse.urljoin(self.base_link, url), output='geturl')
            if self.base_link not in url:
                return url

            header = {'User-Agent': self.user_agent, 'Accept': 'text/html'}
            
            self.__login()
            cookie = self.cookie

            try:
                res = cache.get(client.request, 4, url, headers=header, cookie=cookie, redirect=False, output='geturl')
                if self.base_link not in res:
                    url = res
                else:
                    control.infoDialog("Geschützter Link: Erklärung unter Einstellungen/Konten", sound=True, icon='WARNING')
            except:
                return

            return url
        except:
            source_faultlog.logFault(__name__, source_faultlog.tagResolve)
            return

    def __search(self, titles, year):
        try:
            r = cache.get(client.request, 4, urlparse.urljoin(self.base_link, self.search_link))

            t = [cleantitle.get(i) for i in set(titles) if i]

            links = dom_parser.parse_dom(r, "div", attrs={"class" : "genre"})
            links = dom_parser.parse_dom(links, "a")
            links = [(i.attrs["href"], i.content) for i in links]
            
            links = [i for i in links if any(title in cleantitle.get(i[1]) for title in t)]
            links = [(list(i) + [difflib.SequenceMatcher(None, t[0], cleantitle.get(i[1])).ratio() ]) for i in links]
            links = sorted(links, key = lambda i: i[2])  

            if len(links) > 0:
                return source_utils.strip_domain(links[len(links)-1][0])
            return ""
        except:
            try:
                source_faultlog.logFault(__name__, source_faultlog.tagSearch, titles[0])
            except:
                return
            return

    def __login(self):
        try:
            if (self.login == '' or self.password == ''):
                return

            url = urlparse.urljoin(self.base_link, '/login')
            post = urllib.urlencode({'email': self.login, 'password': self.password, 'autoLogin': 'on'})
            header = {'User-Agent': self.user_agent, 'Accept': 'text/html'}
            cookie = client.request(url, headers=header, referer=url, post=post, output='cookie')
            data = client.request(url, cookie=cookie, output='extended')

            if '/home/logout' in data[0]:
                self.cookie = cookie
                return

            return
        except:
            return
