'''
    urlresolver XBMC Addon
    Copyright (C) 2017

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
'''
from urlresolver.plugins.__generic_resolver__ import GenericResolver

class BitPornoResolver(GenericResolver):
    #print "print UR BitPorno"
    name = 'BitPorno'
    domains = ['bitporno.com']
    pattern = '(?://|\.)(bitporno\.com)/(?:\?v=|embed/)([a-zA-Z0-9]+)'

    def get_url(self, host, media_id):
        print "print UR BitPorno self, host, media_id", self,host, media_id
        print "print return", self._default_get_url(host, media_id, template='http://{host}/?v={media_id}')
        return self._default_get_url(host, media_id, template='http://{host}/?v={media_id}')
        return "https://www.bitporno.com/?v=FM11XRJLMP"

    @classmethod
    def _is_enabled(cls):
        return True