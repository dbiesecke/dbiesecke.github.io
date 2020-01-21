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

import re
import urlparse

from resources.lib.modules import cache
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils
from resources.lib.modules import source_faultlog


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.genre_filter = ['horror']
        self.domains = ['flimmerstube.com', 'horrorkino.do.am']
        self.base_link = 'http://flimmerstube.com'
        self.search_link = 'video/shv'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = cache.get(client.request, 4, urlparse.urljoin(self.base_link, url))
            r = re.findall('''vicode\s*=\s*["'](.*?)["'];''', r)[0].decode('string_escape')
            r = dom_parser.parse_dom(r, 'iframe', req='src')
            r = [i.attrs['src'] for i in r]

            for i in r:
                valid, host = source_utils.is_host_valid(i, hostDict)
                if not valid: continue

                sources.append({'source': host, 'quality': 'SD', 'language': 'de', 'url': i, 'direct': False, 'debridonly': False, 'checkquality': True})

            if len(sources) == 0:
                raise Exception()
            return sources
        except:
            source_faultlog.logFault(__name__,source_faultlog.tagScrape, url)
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year):
        try:
            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = cache.get(client.request, 4, urlparse.urljoin(self.base_link, self.search_link), post={'query': cleantitle.query(titles[0])})

            r = dom_parser.parse_dom(r, 'li', attrs={'class': 'entTd'})
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 've-screen'}, req='title')
            r = [(dom_parser.parse_dom(i, 'a', req='href'), i.attrs['title'].split(' - ')[0]) for i in r]
            r = [(i[0][0].attrs['href'], i[1], re.findall('(.+?) \(*(\d{4})', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y]
            if len(r) > 0:
                r = r[0]
            else:
                return

            return source_utils.strip_domain(r)
        except:
            try:
                source_faultlog.logFault(__name__, source_faultlog.tagSearch, titles[0])
            except:
                return
            return
