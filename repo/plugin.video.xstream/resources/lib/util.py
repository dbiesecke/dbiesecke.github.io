# -*- coding: utf-8 -*-
import htmlentitydefs, re, hashlib, urllib
from resources.lib import pyaes

class cUtil:
    @staticmethod
    def removeHtmlTags(sValue, sReplace=''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)

    @staticmethod
    def formatTime(iSeconds):
        iSeconds = int(iSeconds)

        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if iSeconds < 10:
            iSeconds = '0' + str(iSeconds)

        if iMinutes < 10:
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    @staticmethod
    def urlDecode(sUrl):
        return urllib.unquote(sUrl)

    @staticmethod
    def urlEncode(sUrl):
        return urllib.quote(sUrl)

    @staticmethod
    def unquotePlus(sUrl):
        return urllib.unquote_plus(sUrl)

    @staticmethod
    def quotePlus(sUrl):
        return urllib.quote_plus(sUrl)

    # Removes HTML character references and entities from a text string.
    @staticmethod
    def unescape(text):
        def fixup(m):
            text = m.group(0)
            if not text.endswith(';'): text += ';'
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass

            # replace nbsp with a space
            text = text.replace(u'\xa0', u' ')
            return text

        if isinstance(text, str):
            try:
                text = text.decode('utf-8')
            except:
                try:
                    text = text.decode('utf-8', 'ignore')
                except:
                    pass

        return re.sub("&(\w+;|#x?\d+;?)", fixup, text.strip())

    @staticmethod
    def cleanse_text(text):
        if text is None: text = ''
        text = cUtil.unescape(text)
        text = cUtil.removeHtmlTags(text)
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        return text

    @staticmethod
    def evp_decode(cipher_text, passphrase, salt=None):
        if not salt:
            salt = cipher_text[8:16]
            cipher_text = cipher_text[16:]
        data = cUtil.evpKDF(passphrase, salt)
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(data['key'], data['iv']))
        plain_text = decrypter.feed(cipher_text)
        plain_text += decrypter.feed()
        return plain_text

    @staticmethod
    def evpKDF(passwd, salt, key_size=8, iv_size=4):
        target_key_size = key_size + iv_size
        derived_bytes = ""
        number_of_derived_words = 0
        block = None
        hasher = hashlib.new("md5")
        while number_of_derived_words < target_key_size:
            if block is not None:
                hasher.update(block)
            hasher.update(passwd)
            hasher.update(salt)
            block = hasher.digest()
            hasher = hashlib.new("md5")
            for _i in range(1, 1):
                hasher.update(block)
                block = hasher.digest()
                hasher = hashlib.new("md5")
            derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]
            number_of_derived_words += len(block) / 4
        return {
            "key": derived_bytes[0: key_size * 4],
            "iv": derived_bytes[key_size * 4:]
        }
