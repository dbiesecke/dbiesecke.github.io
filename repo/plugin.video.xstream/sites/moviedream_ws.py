# -*- coding: utf-8 -*-
from resources.lib import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import pyaes
from resources.lib import m as I11I1IIII1II11111II1I1I1II11I1I
import base64


SITE_IDENTIFIER = 'moviedream_ws'
SITE_NAME = 'MovieDream'
SITE_ICON = 'moviedream.png'
URL_MAIN = 'https://moviedream.ws/'

URL_SEARCH = URL_MAIN + 'suchergebnisse.php?text=%s&sprache=Deutsch'


def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('value', 'film')
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMenu'), params)
    params.setParam('value', 'serien')
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showMenu'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showMenu():
    oGui = cGui()
    params = ParameterHandler()
    value = params.getValue('value')
    if value == 'film':
        params.setParam('sUrl', URL_MAIN + 'kino')
        oGui.addFolder(cGuiElement('Kino', SITE_IDENTIFIER, 'showEntries'), params)
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = 'href="(?:\.\.\/)*([neu|beliebt]+%s[^"]*)"[^>]*>([^<]+)<\/a><\/li>' % value
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    for sID, sName in aResult:
        params.setParam('sUrl', URL_MAIN + sID)
        oGui.addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.setEndOfDirectory()


def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    value = params.getValue('value')
    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = 'href="(/%s[^"]+)">([^<]+)' % value
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    for sUrl, sName in aResult:
        params.setParam('sUrl', entryUrl + sUrl)
        oGui.addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    if 'genre' in entryUrl:
        oRequest = cRequestHandler(entryUrl + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=(sGui is not False))
    else:
        oRequest = cRequestHandler(entryUrl + '?p=' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=(sGui is not False))
    
    sHtmlContent = oRequest.request()
    pattern = 'class="linkto.*?href="([^"]+).*?src="([^"]+).*?>([^>]+)</div>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    cf = cRequestHandler.createUrl(entryUrl, oRequest)
    total = len(aResult)
    for sUrl, sThumbnail, sName in aResult:
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        sThumbnail = URL_MAIN + sThumbnail + cf
        isTvshow = True if 'serie' in sUrl else False
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        oGuiElement.setMediaType("tvshow" if isTvshow else "movie")
        params.setParam('entryUrl', URL_MAIN + sUrl.replace('../..',''))
        params.setParam('Name', sName)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('isTvshow', isTvshow)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        sPageNr = int(params.getValue('page'))
        if sPageNr == 0:
            sPageNr = 2
        else:
            sPageNr += 1
        pattern = 'seiterr"[^>]href=".*?([\d]+)'
        isMatch, Lastpage = cParser.parseSingleResult(sHtmlContent, pattern)
        if isMatch:
            if int(sPageNr) <= int(Lastpage):
                params.setParam('page', int(sPageNr))
                oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if 'serie' in entryUrl else 'movies')
        oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = 'href="([^"]+)" class="seasonbutton.*?">([^<]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    isDesc, sDesc = cParser.parse(sHtmlContent, '<p style.*?;">([^"]+)</p>')

    total = len(aResult)
    for sUrl, sSeason in aResult:
        oGuiElement = cGuiElement(sSeason, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(params.getValue('Name'))
        if isDesc:
            oGuiElement.setDescription(sDesc[0])
        oGuiElement.setThumbnail(params.getValue('sThumbnail'))
        oGuiElement.setFanart(params.getValue('sThumbnail'))
        params.setParam('entryUrl', URL_MAIN + sUrl.replace('../..',''))
        oGui.addFolder(oGuiElement, params, True, total)
    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    sTVShowTitle = params.getValue('Name')
    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = 'href="([^"]+)" class="episodebutton" id="episodebutton\d+">#([\d]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    sHtmlContent = cRequestHandler(entryUrl).request()
    isDesc, sDesc = cParser.parse(sHtmlContent, '<p style.*?;">([^"]+)</p>')

    total = len(aResult)
    for sUrl, sEpisode in aResult:
        oGuiElement = cGuiElement('Folge ' + sEpisode, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('season')
        oGuiElement.setEpisode(sEpisode)
        oGuiElement.setMediaType('episode')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        if isDesc:
            oGuiElement.setDescription(sDesc[0])
        oGuiElement.setThumbnail(params.getValue('sThumbnail'))
        oGuiElement.setFanart(params.getValue('sThumbnail'))
        params.setParam('entryUrl', URL_MAIN + sUrl.replace('../..',''))
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showHosters():
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = '''writesout[^>]'([^']+).*?"y":"([^"]+).*?fast":"([^"]+).*?bald":"([^"]+)'''
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)

    hosters = []
    if not isMatch:
        return hosters

    for password, ciphertext, iv, salt in aResult:
        hoster = {}
        key = I11I1IIII1II11111II1I1I1II11I1I.I11I1IIII1II11111II1I1I1II11III(salt)
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv.decode('hex')))
        decrypted = decrypter.feed(base64.b64decode(ciphertext))  + decrypter.feed()
        sUrl = decrypted
        if not 'nurhdfilm' in sUrl.lower():
            hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
            hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % sSearchText, oGui, sSearchText)
