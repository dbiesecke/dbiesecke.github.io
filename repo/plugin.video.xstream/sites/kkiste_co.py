# -*- coding: utf-8 -*-
from resources.lib import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'kkiste_co'
SITE_NAME = 'KKiste.co'
SITE_ICON = 'kkiste_co.png'

URL_MAIN = 'https://kkiste.co/'


def load():
    logger.info('Load %s' % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showGenre():
    params = ParameterHandler()
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = 'nav-list fx-row">.*?</ul>'
    isMatch, sHtmlContainer = cParser.parseSingleResult(sHtmlContent, pattern)

    if isMatch:
        isMatch, aResult = cParser.parse(sHtmlContainer, 'href="([^"]+).*?>([^<]+)')
    if not isMatch:
        cGui().showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    for sUrl, sName in aResult:
        params.setParam('sUrl', sUrl)
        cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if sSearchText:
        oRequest.addParameters('do', 'search')
        oRequest.addParameters('subaction', 'search')
        oRequest.addParameters('story', sSearchText)
        oRequest.setRequestType(1)
    sHtmlContent = oRequest.request()
    pattern = 'class="short">.*?href="([^"]+)">([^<]+).*?img src="([^"]+).*?desc">([^<]+).*?Jahr.*?([\d]+).*?s-red">([\d]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    cf = cRequestHandler.createUrl(entryUrl, oRequest)
    total = len(aResult)
    for sUrl, sName, sThumbnail, sDesc, sYear, sDuration in aResult:
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        sThumbnail =  URL_MAIN + sThumbnail + cf
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setYear(sYear)
        oGuiElement.setDescription(sDesc)
        oGuiElement.addItemValue('duration', sDuration)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, False, total)
    if not sGui:
        isMatchNextPage, sNextUrl = cParser().parseSingleResult(sHtmlContent, 'next"><a href="([^"]+)')
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('movie')
        oGui.setEndOfDirectory()


def showHosters():
    sUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    isMatch, aResult = cParser().parse(sHtmlContent, 'link="([^"]+)')
    hosters = []
    if isMatch:
        for sUrl in aResult:
            if not 'vod' in sUrl and not 'youtube' in sUrl and not 'verystream' in sUrl:
                if sUrl.startswith('http'):
                    hoster = {'link': sUrl, 'name': cParser.urlparse(sUrl)}
                else:
                    hoster = {'link': 'https:' + sUrl, 'name': cParser.urlparse(sUrl)}
                hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    if 'supervideo' in sUrl:
        sUrl = supervideo(sUrl)
        return [{'streamUrl': sUrl, 'resolved': True}]
    else:
        return [{'streamUrl': sUrl, 'resolved': False}]


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    if not sSearchText: return
    showEntries(URL_MAIN, oGui, sSearchText)


def supervideo(sUrl):
    sHtmlContent = cRequestHandler(sUrl).request()
    import jsunpacker
    isMatch, aResult = cParser().parse(sHtmlContent, '(eval\(function.*?)</script>')
    if isMatch:
        for packed in aResult:
            sHtmlContent += jsunpacker.unpack(packed)
        isMatch, sUrl = cParser().parse(sHtmlContent, 'sources.*?"([^"]+)')
    else:
        isMatch, sUrl = cParser().parse(sHtmlContent, 'player.updateSrc\({src: \"([^\"]+?)\"')
    return sUrl[0]
