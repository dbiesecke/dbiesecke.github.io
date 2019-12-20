# -*- coding: utf-8 -*-
import re, sys, urllib2
from binascii import hexlify, unhexlify
from urlparse import urlparse
from resources.lib import logger, pyaes, cookie_helper
from resources.lib.parser import cParser


class cBFScrape:
    COOKIE_NAME = 'BLAZINGFAST-WEB-PROTECT'

    def resolve(self, url, cookie_jar, user_agent):
        headers = {'User-agent': user_agent, 'Referer': url}

        try:
            cookie_jar.load(ignore_discard=True)
        except Exception as e:
            logger.info(e)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

        request = urllib2.Request(url)
        for key in headers:
            request.add_header(key, headers[key])

        try:
            response = opener.open(request)
        except urllib2.HTTPError as e:
            response = e

        body = response.read()

        cookie_jar.extract_cookies(response, request)
        cookie_helper.check_cookies(cookie_jar)

        pattern = 'xhr\.open\("GET","([^,]+),'
        match = cParser.parse(body, pattern)
        if not match[0]:
            return
        urlParts = match[1][0].split('"')
        parsed_url = urlparse(url)
        sid = '1200'
        script_url = '%s://%s%s%s%s' % (parsed_url.scheme, parsed_url.netloc, urlParts[0], sid, urlParts[2])
        request = urllib2.Request(script_url)
        for key in headers:
            request.add_header(key, headers[key])
        try:
            response = opener.open(request)
        except urllib2.HTTPError as e:
            response = e

        body = response.read()
        cookie_jar.extract_cookies(response, request)
        cookie_helper.check_cookies(cookie_jar)

        if not self.checkBFCookie(body):
            return body  # even if its false its probably not the right content, we'll see
        cookie = self.getCookieString(body)
        if not cookie:
            return

        name, value = cookie.split(';')[0].split('=')
        cookieData = dict((k.strip(), v.strip()) for k, v in (item.split("=") for item in cookie.split(";")))
        cookie = cookie_helper.create_cookie(name, value, domain=cookieData['domain'], expires=sys.maxint, discard=False)
        cookie_jar.set_cookie(cookie)
        request = urllib2.Request(url)
        for key in headers:
            request.add_header(key, headers[key])

        try:
            response = opener.open(request)
        except urllib2.HTTPError as e:
            response = e
        return response

    def checkBFCookie(self, content):
        """
        returns True if there seems to be a protection
        """
        return cBFScrape.COOKIE_NAME in content

    # not very robust but lazieness...
    def getCookieString(self, content):
        vars = re.findall('toNumbers\("([^"]+)"', content)
        if not vars:
            logger.info('vars not found')
            return False
        value = self._decrypt(vars[2], vars[0], vars[1])
        if not value:
            logger.info('value decryption failed')
            return False
        pattern = '"%s=".*?";([^"]+)"' % cBFScrape.COOKIE_NAME
        cookieMeta = re.findall(pattern, content)
        if not cookieMeta:
            logger.info('cookie meta not found')
        cookie = "%s=%s;%s" % (cBFScrape.COOKIE_NAME, value, cookieMeta[0])
        return cookie
        # + toHex(BFCrypt.decrypt(c, 2, a, b)) +

    def _decrypt(self, msg, key, iv):
        msg = unhexlify(msg)
        key = unhexlify(key)
        iv = unhexlify(iv)
        if len(iv) != 16:
            logger.info("iv length is" + str(len(iv)) + " must be 16.")
            return False
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
        plain_text = decrypter.feed(msg)
        plain_text += decrypter.feed()
        f = hexlify(plain_text)
        return f
