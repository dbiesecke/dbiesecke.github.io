#-*- coding: utf-8 -*-
import re, os, sys, time, hashlib, socket
import xbmcgui

from resources.lib.config import cConfig
from resources.lib import logger, common

try:
    from urlparse import urlparse
    from urllib import quote, urlencode
    from urllib2 import HTTPError, URLError, HTTPHandler, HTTPSHandler, HTTPCookieProcessor, build_opener, Request, urlopen
    from cookielib import LWPCookieJar
    from httplib import HTTPSConnection
except ImportError:
    from urllib.parse import quote, urlencode, urlparse
    from urllib.error import HTTPError, URLError
    from urllib.request import HTTPHandler, HTTPSHandler, HTTPCookieProcessor, build_opener, Request, urlopen
    from http.cookiejar import LWPCookieJar
    from http.client import HTTPSConnection


class cRequestHandler:
    def __init__(self, sUrl, caching=True, ignoreErrors=False, compression=True):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__aParameters = {}
        self.__aResponses = {}
        self.__headerEntries = {}
        self.__cachePath = ''
        self._cookiePath = ''
        self.ignoreDiscard(False)
        self.ignoreExpired(False)
        self.caching = caching
        self.ignoreErrors = ignoreErrors
        self.compression = compression
        self.cacheTime = int(cConfig().getSetting('cacheTime', 600))
        self.requestTimeout = int(cConfig().getSetting('requestTimeout', 60))
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.setCachePath()
        self.__setCookiePath()
        self.__sResponseHeader = ''
        if self.requestTimeout >= 60 or self.requestTimeout <= 10:
            self.requestTimeout = 60

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self.__cType = cType

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        self.__headerEntries[sHeaderKey] = sHeaderValue

    def getHeaderEntry(self, sHeaderKey):
        if sHeaderKey in self.__headerEntries:
            return self.__headerEntries[sHeaderKey]

    def addParameters(self, key, value, quote2=False):
        if not quote2:
            self.__aParameters[key] = value
        else:
            self.__aParameters[key] = quote(str(value))

    def addResponse(self, key, value):
        self.__aResponses[key] = value

    def getResponseHeader(self):
        return self.__sResponseHeader

    def getRealUrl(self):
        return self.__sRealUrl

    def request(self):
        self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest()

    def getRequestUri(self):
        return self.__sUrl + '?' + urlencode(self.__aParameters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0')
        self.addHeaderEntry('Accept-Language', 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3')
        self.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        if self.compression:
            self.addHeaderEntry('Accept-Encoding', 'gzip')

    def GetCookies(self):
        if not self.__sResponseHeader:
            return ''
        if 'Set-Cookie' in self.__sResponseHeader:
            c = self.__sResponseHeader.get('set-cookie')
            c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',c)
            if c2:
                cookies = ''
                for cook in c2:
                    cookies = cookies + cook[0] + '=' + cook[1]+ ';'
                cookies = cookies[:-1]
                return cookies
        return ''

    def __callRequest(self):
        if self.caching and self.cacheTime > 0:
            sContent = self.readCache(self.getRequestUri())
            if sContent:
                return sContent

        cookieJar = LWPCookieJar(filename=self._cookiePath)
        try:
            cookieJar.load(ignore_discard=self.__bIgnoreDiscard, ignore_expires=self.__bIgnoreExpired)
        except Exception as e:
            logger.info(e)

        sParameters = urlencode(self.__aParameters, True)
        handlers = [HTTPHandler(), HTTPSHandler(), HTTPCookieProcessor(cookiejar=cookieJar)]

        if (2, 7, 9) <= sys.version_info < (2, 7, 11):
            handlers.append(newHTTPSHandler)
        opener = build_opener(*handlers)
        if (len(sParameters) > 0):
            oRequest = Request(self.__sUrl, sParameters)
        else:
            oRequest = Request(self.__sUrl)

        for key, value in list(self.__headerEntries.items()):
            oRequest.add_header(key, value)
        cookieJar.add_cookie_header(oRequest)


        sContent = ''
        try:
            oResponse = opener.open(oRequest, timeout=self.requestTimeout)
            sContent = oResponse.read().encode('ascii')
            self.__sResponseHeader = oResponse.info()

            #compressed page ?
            if self.__sResponseHeader.get('Content-Encoding') == 'gzip':
                import zlib
                sContent = zlib.decompress(sContent, zlib.MAX_WBITS|16)

            #https://bugs.python.org/issue4773
            self.__sRealUrl = oResponse.geturl()
            self.__sResponseHeader = oResponse.info()
            oResponse.close()

            oResponse = opener.open(oRequest, timeout=self.requestTimeout)
        except HTTPError as e:
            if e.code == 503:
                from resources.lib import cloudflare

                if cloudflare.CheckIfActive(e.read()):
                    self.__sResponseHeader = e.hdrs
                    cookies = self.GetCookies()
                    CF = cloudflare.CloudflareBypass()
                    sContent = CF.GetHtml(self.__sUrl,e.read(),cookies,sParameters,oRequest.headers)
                    self.__sRealUrl, self.__sResponseHeader = CF.GetReponseInfo()
                else:
                    sContent = e.read()
                    self.__sRealUrl = e.geturl()
                    self.__sResponseHeader = e.headers()
            else:
                try:
                    if not self.ignoreErrors:
                        print(('xStream', 'Fehler beim Abrufen der Url:', self.__sUrl))
                    self.__sRealUrl = e.geturl()
                    self.__sResponseHeader = e.headers
                    sContent = e.read()           
                except:
                    sContent = ''

            if not sContent:
                if not self.ignoreErrors:
                    print(('xStream', 'Fehler beim Abrufen der Url:', self.__sUrl))
                return ''

        except URLError as e:
            if not self.ignoreErrors:
                if hasattr(e.reason, 'args') and e.reason.args[0] == 1 and sys.version_info < (2, 7, 9):
                    xbmcgui.Dialog().ok('xStream', str(e.reason), '', 'For this request is Python v2.7.9 or higher required.')
                else:
                    xbmcgui.Dialog().ok('xStream', str(e.reason))
            logger.error("URLError " + str(e.reason) + " Url: " + self.__sUrl)

        cookieJar.save(ignore_discard=self.__bIgnoreDiscard, ignore_expires=self.__bIgnoreExpired)
        if (self.__bRemoveNewLines == True):
            sContent = sContent.replace("\n","")
            sContent = sContent.replace("\r\t","")

        if (self.__bRemoveBreakLines == True):
            sContent = sContent.replace("&nbsp;","")

        if self.caching and self.cacheTime > 0:
            self.writeCache(self.getRequestUri(), sContent)
            return sContent

    def getHeaderLocationUrl(self):
        opened = urlopen(self.__sUrl)
        return opened.geturl()

    def __setCookiePath(self):
        profilePath = common.profilePath
        cookieFile = os.path.join(profilePath, 'cookies.txt')
        if not os.path.exists(cookieFile):
            file = open(cookieFile, 'w')
            file.close()
        self._cookiePath = cookieFile

    def getCookie(self, sCookieName, sDomain=''):
        cookieJar = LWPCookieJar()
        try:
            cookieJar.load(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
        except Exception as e:
            logger.info(e)

        for entry in cookieJar:
            if entry.name == sCookieName:
                if sDomain == '':
                    return entry
                elif entry.domain == sDomain:
                    return entry
        return False

    def setCookie(self, oCookie):
        cookieJar = LWPCookieJar()
        try:
            cookieJar.load(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)
        except Exception as e:
            logger.info(e)
        cookieJar.set_cookie(oCookie)
        cookieJar.save(self._cookiePath, self.__bIgnoreDiscard, self.__bIgnoreExpired)

    def ignoreDiscard(self, bIgnoreDiscard):
        self.__bIgnoreDiscard = bIgnoreDiscard

    def ignoreExpired(self, bIgnoreExpired):
        self.__bIgnoreExpired = bIgnoreExpired

    #   Caching
    def setCachePath(self, cache=''):
        if not cache:
            profilePath = common.profilePath
            cache = os.path.join(profilePath, 'htmlcache')
        if not os.path.exists(cache):
            os.makedirs(cache)
        self.__cachePath = cache

    def readCache(self, url):
        h = hashlib.md5(url.encode('utf-8')).hexdigest()
        cacheFile = os.path.join(self.__cachePath, h)
        fileAge = self.getFileAge(cacheFile)
        if 0 < fileAge < self.cacheTime:
            try:
                fhdl = file(cacheFile, 'r')
                content = fhdl.read()
            except:
                logger.info('Could not read Cache')
            if content:
                logger.info('read html for %s from cache' % url)
                return content
        return ''

    def writeCache(self, url, content):
        h = hashlib.md5(url).hexdigest()
        cacheFile = os.path.join(self.__cachePath, h)
        try:
            fhdl = file(cacheFile, 'w')
            fhdl.write(content)
        except:
            logger.info('Could not write Cache')

    @staticmethod
    def getFileAge(cacheFile):
        try:
            fileAge = time.time() - os.stat(cacheFile).st_mtime
        except:
            return 0
        return fileAge

    def clearCache(self):
        files = os.listdir(self.__cachePath)
        for file in files:
            cacheFile = os.path.join(self.__cachePath, file)
            fileAge = self.getFileAge(cacheFile)
            if fileAge > self.cacheTime:
                os.remove(cacheFile)

    def Readcookie(self,Domain):
        PathCache = common.profilePath
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        try:
            file = open(Name,'r')
            data = file.read()
            file.close()
        except:
            return ''
        return data

    @staticmethod
    def createUrl(sUrl, oRequest):
        import re
        parsed_url = urlparse(sUrl)
        netloc = parsed_url.netloc[4:] if parsed_url.netloc.startswith('www.') else parsed_url.netloc
        cookies = oRequest.Readcookie(netloc.replace('.', '_'))
        cfId = re.compile('__cfduid=([^;]+)', re.DOTALL).findall(cookies)
        cfClear = re.compile('cf_clearance=([^;]+)', re.DOTALL).findall(cookies)
        sUrl = ''
        if cfId and cfClear and 'Cookie=Cookie:' not in sUrl:
            delimiter = '&' if '|' in sUrl else '|'
            sUrl = delimiter + "Cookie=Cookie: __cfduid=" + cfId[0] + "; cf_clearance=" + cfClear[0]
        if 'User-Agent=' not in sUrl:
            delimiter = '&' if '|' in sUrl else '|'
            sUrl += delimiter + "User-Agent=" + 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
        return sUrl


# python 2.7.9 and 2.7.10 certificate workaround
class newHTTPSHandler(HTTPSHandler):
    def do_open(self, conn_factory, req, **kwargs):
        conn_factory = newHTTPSConnection
        return HTTPSHandler.do_open(self, conn_factory, req)


class newHTTPSConnection(HTTPSConnection):
    def __init__(self, host, port=None, key_file=None, cert_file=None, strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, context=None):
        import ssl
        context = ssl._create_unverified_context()
        HTTPSConnection__init__(self, host, port, key_file, cert_file, strict, timeout, source_address, context)
