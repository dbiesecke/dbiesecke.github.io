"""
urlresolver XBMC Addon
Copyright (C) 2011 t0mm0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import time
from lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class XvidstageResolver(UrlResolver):
    name = "xvidstage"
    domains = ["xvidstage.com", "faststream.ws"]
    pattern = '(?://|\.)((?:xvidstage\.com|faststream\.ws))/(?:embed-)?([0-9A-Za-z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        
        #print "print UR xvid getmediaurl self, host, media_id", self,host, media_id
        web_url = self.get_url(host, media_id)
        
        #print "print UR xvid web_url", web_url
        headers = {'User-Agent': common.FF_USER_AGENT}
        response = self.net.http_GET(web_url, headers=headers)
        
        html = response.content
        #print "print UR xvid html", html
        data = helpers.get_hidden(html)
        headers['Cookie'] = response.get_headers(as_dict=True).get('Set-Cookie', '')
        time.sleep(11)
        html = self.net.http_POST(web_url, headers=headers, form_data=data).content
        
        if html:
            packed = helpers.get_packed_data(html)

            sources = helpers.scrape_sources(packed, result_blacklist=['tmp'])
            if sources: return helpers.pick_source(sources) + helpers.append_headers(headers)

        raise ResolverError('Unable to locate video')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://www.xvidstage.com/{media_id}')
