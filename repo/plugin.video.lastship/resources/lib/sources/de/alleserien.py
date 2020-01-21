# -*- coding: utf-8 -*-

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
import datetime
import urllib

try:
    from providerModules.LastShip import cache
    from providerModules.LastShip import cleantitle
    from providerModules.LastShip import dom_parser
    from providerModules.LastShip import source_utils
    from providerModules.LastShip import client
except:
    from resources.lib.modules import cache
    from resources.lib.modules import cleantitle
    from resources.lib.modules import dom_parser
    from resources.lib.modules import source_utils
    from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.url_domain = self.url_domain_checker(url='https://www.allestream.com', slash=True, headers={})
        self.base_link = self.url_domain[0]
        self.domains = [self.url_domain[1]]
        self.search_link = '/search?search=%s'
        self.search_link_query = self.base_link + '/searchPagination'
        self.link_url = '/getpart'
        self.link_url_movie = '/film-getpart'

    def url_domain_checker(self, url, slash, headers):
        geturl = client.request(url, headers=headers, output='geturl')
        if not url == geturl:url = geturl
        domain = urlparse.urlparse(url).netloc
        if slash == False and url.endswith('/'):url = url[:-1]
        elif slash == True and not url.endswith('/'):url = url + '/'
        return (url, domain)

    def movie(self, imdb, title, localtitle, aliases, year):
        titles = source_utils.get_titles_for_search(title, localtitle, aliases)
        url = self.__search(titles)
        if url:
            return url
        return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        titles = source_utils.get_titles_for_search(tvshowtitle, localtvshowtitle, aliases)
        url = self.__search(titles)
        if url:
            return url
        return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = urlparse.urljoin(self.base_link, url)

            r = cache.get(client.request, 8, url)

            seasons = dom_parser.parse_dom(r, "div", attrs={"class": "section-watch-season"})
            seasons = seasons[len(seasons)-int(season)]
            episodes = dom_parser.parse_dom(seasons, "tr")
            episodes = [(dom_parser.parse_dom(i, "th")[0].content, i.attrs["onclick"]) for i in episodes if "onclick" in i.attrs]
            episodes = [re.findall("'(.*?)'", i[1])[0] for i in episodes if i[0] == episode][0]

            return source_utils.strip_domain(episodes)
        except:
            pass

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources
            url = urlparse.urljoin(self.base_link, url)
            content = client.request(url)

            links = dom_parser.parse_dom(content, 'tr', attrs={'class': 'partItem'})
            links = [(i.attrs['data-id'], i.attrs['data-controlid'], re.findall("(.*)\.png", i.content)[0].split("/")[-1]) for i in
                     links if 'data-id' in i[0]]

            temp = [i for i in links if i[2].lower() == 'vip']
            for id, controlId, host in temp:
                link = self.resolve((url, id, controlId, 'film' in url))

                params = {
                    'Referer': url,
                    'Host': 'alleserienplayer.com'
                }
                result = client.request(link, headers=params)
                result = ((re.findall('"(.*?)"', result)[1]).replace('\\x', '').decode("hex")).decode('base64')
                fp = re.findall('FirePlayer_holaplayer."(.*?)"', result)[0]

                posturl = 'https://alleserienplayer.com/fireplayer/video/%s?do=getVideo ' % fp
                data = {'hash': fp, "r": url}
                params = {
                    'Host': 'alleserienplayer.com',
                    'Origin': 'https://alleserienplayer.com',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                result = client.request(posturl, post=data, headers=params)
                result = json.loads(result)
                result = result['videoSources']

                for i in result:
                    if '1080' in i['label']:
                        sources.append({'source': 'CDN', 'quality': '1080p', 'language': 'de', 'url': i['file'], 'direct': True, 'debridonly': False, 'checkquality': False}) 
                    elif '720' in i['label']:
                        sources.append({'source': 'CDN', 'quality': '720p', 'language': 'de', 'url': i['file'], 'direct': True, 'debridonly': False, 'checkquality': False}) 
                    else:
                        sources.append({'source': 'CDN', 'quality': 'SD', 'language': 'de', 'url': i['file'], 'direct': True, 'debridonly': False, 'checkquality': False}) 
            
            links = [i for i in links if i[2].lower() != 'vip']
            for i in links:
                multiPart = re.findall('(.*?)-part-\d+', i[2])
                if(len(multiPart) > 0):
                    links = [(i[0], i[1], i[2] + '-part-1' if i[2] == multiPart[0] else i[2]) for i in links]

            links = [(i[0], i[1], re.findall('(.*?)-part-\d+', i[2])[0] if len(re.findall('\d+', i[2])) > 0 else i[2], 'Multi-Part ' + re.findall('\d+', i[2])[0] if len(re.findall('\d+', i[2])) > 0 else None) for i in links]

            for id, controlId, host, multiPart in links:
                valid, hoster = source_utils.is_host_valid(host, hostDict)
                if not valid: continue

                sources.append({'source': hoster, 'quality': 'SD', 'language': 'de', 'url': (url, id, controlId, 'film' in url), 'info': multiPart if multiPart else '', 'direct': False, 'debridonly': False, 'checkquality': False})

            if len(sources) == 0:
                raise Exception()


            return sources
        except:

            return sources

    def resolve(self, url):
        try:
            if 'google' in url:
                return url
            url, id, controlId, movieSearch = url

            content = client.request(url)
            token = re.findall("_token':'(.*?)'", content)[0]

            params = {
                '_token': token,
                'PartID': id,
                'ControlID': controlId
            }

            link = urlparse.urljoin(self.base_link, self.link_url_movie if movieSearch else self.link_url)
            result = client.request(link, post=params)
            if 'false' in result:
                return
            else:
                return dom_parser.parse_dom(result, 'iframe')[0].attrs['src']
        except:

            return

    def __search(self, titles):
        t = [cleantitle.get(i) for i in set(titles) if i]
        for title in titles:
            try:
                title = title = str(title).split('\'')[0]
                title = urllib.quote(cleantitle.query(title))
                query = self.search_link % title
                query = urlparse.urljoin(self.base_link, query)
                result_search = client.request(query, referer=self.base_link, headers={'Upgrade-Insecure-Requests: 1'})
                token = re.findall('_token\':\'(.*?)\'', result_search)[0]

                data = {'_token': token, "page": "1", "from": "1900", "to": "2018", "type": "Alle", "rating": "0", "sortBy": "latest", "search": title}
                referer = '%s/search?page=1&from=1900&to=2018&type=Alle&rating=0&sortBy=latest&search=%s' % (self.base_link, title)
                result = client.request(self.search_link_query, post=data, headers={'X-Requested-With': 'XMLHttpRequest'}, referer=referer )
                result = result.replace('\\', '')
                links = dom_parser.parse_dom(result, 'a')
                links = [(i.attrs['href'].replace('"', ''), i.attrs['title'].replace('"', '')) for i in links if 'href' in i.attrs and 'title' in i.attrs]
                links = [i[0] for i in links if cleantitle.get(i[1]) in t]
                if len(links) > 0:
                    return source_utils.strip_domain(links[0])
            except:
                pass
