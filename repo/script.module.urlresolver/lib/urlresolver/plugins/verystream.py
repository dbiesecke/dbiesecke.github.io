'''
    urlresolver Kodi plugin
    Copyright (C) 2019

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
'''

import re
from lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class VeryStreamResolver(UrlResolver):
    name = "verystream"
    domains = ["verystream.com"]
    pattern = '(?://|\.)(verystream\.com)/(?:stream|e)/([a-zA-Z0-9]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA,
                   'Referer': web_url}
        response = self.net.http_GET(web_url, headers=headers)
        html = response.content
        r = re.search('videolink">(.*?)</', html)
        if r:
            videosource = 'https://verystream.com/gettoken/%s' % r.group(1)
            return videosource + helpers.append_headers(headers)
        else:
            web_url = web_url.replace('/stream/', '/e/')
            response = self.net.http_GET(web_url, headers=headers)
            html = response.content
            r = re.search('videolink">(.*?)</', html)
            if r:
                videosource = 'https://verystream.com/gettoken/%s' % r.group(1)
                return videosource + helpers.append_headers(headers)
        raise ResolverError("Could not locate video")

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, 'https://verystream.com/stream/{media_id}')
