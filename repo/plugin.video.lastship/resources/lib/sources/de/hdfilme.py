# -*- coding: UTF-8 -*-

"""
    IF/LS/SE Add-on (C) 2019 / ka
    Credits to Lastship, Exodus and Covenant; our thanks go to their creators

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

import json
import re
import urlparse
import urllib

try:
    from providerModules.LastShip import cache
    from providerModules.LastShip import cleantitle
    from providerModules.LastShip import dom_parser
    from providerModules.LastShip import source_utils
    from providerModules.LastShip import directstream
    from providerModules.LastShip import client
except ImportError:
    from resources.lib.modules import cache
    from resources.lib.modules import cleantitle
    from resources.lib.modules import dom_parser
    from resources.lib.modules import source_utils
    from resources.lib.modules import directstream
    from resources.lib.modules import client

## Test cloudscraper
#try: import cloudscraper as cfscrape
#except ImportError: import cfscrape
import cfscrape

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['hdfilme.cc']
        self.base_link = 'https://hdfilme.cc'
        self.search_link = '/search?key=%s'
        self.search_api = self.base_link + '/search'
        self.get_link = 'movie/load-stream/%s/%s?'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        titles = source_utils.get_titles_for_search(title, localtitle, aliases)
        url = self.__search(titles, year)
        if url:
            return url
        return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            return {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle,
                    'aliases': aliases, 'year': year}
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            data = url
            titles = source_utils.get_titles_for_search(data['tvshowtitle'], data['localtvshowtitle'], data['aliases'])
            url = self.__search(titles, data['year'], season)
            if not url: return
            urlWithEpisode = url + '/folge-%s' % episode
            return source_utils.strip_domain(urlWithEpisode)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url: return sources
            query = urlparse.urljoin(self.base_link, url)
            headers = {'Host': self.domains[0], 'Upgrade-Insecure-Requests': '1'}
            moviecontent = self.scraper.get(query, headers=headers).content

            url = url.replace('-info', '-stream')
            r = re.findall('(\d+)-stream(?:\?folge-(\d+))?', url)
            r = [(i[0], i[1] if i[1] else '1') for i in r][0]
            if "folge" in url:
                streamlink = re.findall(r'data-episode-id="(.*?)"', moviecontent)
                episode = int(re.findall(r'\/folge-(\d+)', url)[0])
                r = (r[0], streamlink[episode - 1])
            else:
                streamlink = dom_parser.parse_dom(moviecontent, 'a', attrs={'class': 'new'})
                episode = int(re.findall(r'data-episode-id="(.*?)"', moviecontent)[0])
                r = (r[0], episode)

            headers = {'Host': self.domains[0], 'X-Requested-With': 'XMLHttpRequest',
                       'referer': urlparse.urljoin(self.base_link, url)}

            for server in ['', 'server=2']:
                link = self.get_link + server
                moviesource = self.scraper.get(urlparse.urljoin(self.base_link, link % r), headers=headers)
                if server == '':
                    foundsource = re.findall('window.urlVideo = (\".*?\");', moviesource.content)
                    sourcejson = json.loads(foundsource[0])
                    streamssources = self.scraper.get(sourcejson).content
                    streams = re.findall(r'/drive(.*?)\n', streamssources)
                    qualitys = re.findall(r'RESOLUTION=(.*?)\n', streamssources)
                    url_stream = re.findall(r'"(.*?)"', foundsource[0])

                    for x in range(0, len(qualitys)):
                        stream = ('/drive' + streams[x])
                        stream = urlparse.urljoin(url_stream[0], stream)
                        params = {'Referer': url, 'Origin': self.base_link}
                        content = client.request(stream, headers=params)
                        if 'Not ready' in content: continue

                        if "1080" in qualitys[x]:
                            sources.append({'source': 'HDFILME.CC', 'quality': '1080p', 'language': 'de',
                                            'url': stream, 'direct': True,
                                            'debridonly': False})
                        elif "720" in qualitys[x]:
                            sources.append({'source': 'HDFILME.CC', 'quality': '720p', 'language': 'de',
                                            'url': stream, 'direct': True,
                                            'debridonly': False})
                        else:
                            sources.append({'source': 'HDFILME.CC', 'quality': 'SD', 'language': 'de',
                                            'url': stream, 'direct': True,
                                            'debridonly': False})

                foundsource = re.findall('var sources = (\[.*?\]);', moviesource.content)
                if any(foundsource):
                    foundsource = re.findall('sources\s=\s(\[{(.|\n|\r)*?\])', moviesource.content)[0]

                sourcejson = json.loads(foundsource[0].replace('\'', '"'))

                for sourcelink in sourcejson:
                    try:
                        tag = directstream.googletag(sourcelink['file'])
                        if tag:
                            sources.append({'source': 'gvideo', 'quality': tag[0].get('quality', 'SD'), 'language': 'de',
                                            'url': sourcelink['file'], 'direct': True, 'debridonly': False})
                        else:
                            if sourcelink['label'] == 'm3u8':
                                quality = "720p"
                            else:
                                quality = sourcelink['label']
                            sources.append({'source': 'CDN', 'quality': '720p', 'language': 'de', 'url': sourcelink['file'],
                                            'direct': True, 'debridonly': False})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year, season='0'):
        t = [cleantitle.get(i) for i in set(titles) if i]
        for title in titles:
            try:
                title = cleantitle.query(title)
                query = self.search_link % (urllib.quote_plus(title))
                query = urlparse.urljoin(self.base_link, query)
                headers = {'Referer': self.base_link + '/', 'Host': self.domains[0], 'Upgrade-Insecure-Requests': '1'}
                if season == "0":
                    content = self.scraper.get(query, headers=headers).content
                    searchResult = dom_parser.parse_dom(content, 'div', attrs={'class': 'body-section'})
                    results = re.findall(r'title-product.*?href=\"(.*?)\" title=\"(.*?)\"\>.*?(\d{4})',
                                         searchResult[0].content, flags=re.DOTALL)
                    for x in range(0, len(results)):
                        if year in results[x][2]:
                            title = cleantitle.get(results[x][1])
                            if any(i in title for i in t):
                                url = source_utils.strip_domain(results[x][0]) + '/deutsch'
                                return url
                else:
                    #content = self.scraper.get(query, headers=headers).content
                    content = cache.get(self.scraper.get, 48, query, headers=headers).content
                    searchResult = dom_parser.parse_dom(content, 'div', attrs={'class': 'body-section'})
                    results = re.findall(r'title-product.*?href=\"(.*?)\" title=\"(.*?)\"\>.*?(\d{4})',
                                         searchResult[0].content, flags=re.DOTALL)
                    for x in range(0, len(results)):
                        title = cleantitle.get(results[x][1])
                        if any(i in title for i in t):
                            if "staffel0" + str(season) in title or "staffel" + str(season) in title:
                                if not 'special' in title and not 'special' in i:
                                    url = source_utils.strip_domain(results[x][0])
                                    return url
            except:
                return
