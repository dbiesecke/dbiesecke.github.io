"""
    Kodi urlresolver plugin
    Copyright (C) 2016  script.module.urlresolver

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

     Resolver HDGO VIO - 12.05.2019 - RC 1 incl. select resolution 
"""
import re
import xbmcgui
from lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class HdgoResolver(UrlResolver):
    name = "hdgo"
    domains = ["hdgo.cc", "vio.to"]
    pattern = '(?://|\.)((?:hdgo|vio)\.(?:cc|to))/video/t/([a-zA-Z0-9/]+)'


    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA,
                   'Referer': web_url}
        html = self.net.http_GET(web_url, headers=headers).content
        match = re.findall('url:.*?\'(.+?)\'', html)

        if match:
            sources = ["https:" + i for i in match if i[:2] == "//"]
            if len(sources) == 1:
                return sources[0] + helpers.append_headers(headers)
            elif len(sources) > 1:
                options = []
                for i, source in enumerate(sources):
                    quality = ["Low", "SD", "720p", "1080p", "1440p", "4K"]
                    options.append(str(0) + str(i + 1)  + ' | ' + host.upper() + ' | ' + quality[i])
                #result = xbmcgui.Dialog().select('UrlResolver', options)
                result = len(options)-1
                if result == -1:
                    raise ResolverError(common.i18n('no_link_selected'))
                else:
                    return sources[result] + '?quali=' + quality[len(options)-1] + helpers.append_headers(headers)
            else:
                raise ResolverError("Could not locate video")
            
        raise ResolverError("Could not locate video")
    
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/video/t/{media_id}')
