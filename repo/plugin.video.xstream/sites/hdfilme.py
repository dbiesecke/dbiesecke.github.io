# -*- coding: utf-8 -*-
from resources.lib import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler2 import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'hdfilme'
SITE_NAME = 'HDfilme'
SITE_ICON = 'hdfilme.png'

URL_MAIN = 'https://hdfilme.cc'
URL_MOVIES = URL_MAIN + '/filme1?'
URL_SHOWS = URL_MAIN + '/serien1?'
URL_SEARCH = URL_MAIN + '/movie-search?key=%s'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMenu'), params)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showMenu'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showMenu():
    oGui = cGui()
    params = ParameterHandler()
    baseURL = params.getValue('sUrl')
    params.setParam('sUrl', baseURL + 'sort=top&sort_type=desc')
    oGui.addFolder(cGuiElement('Update', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + 'sort=year&sort_type=desc')
    oGui.addFolder(cGuiElement('Year', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + 'sort=name&sort_type=desc')
    oGui.addFolder(cGuiElement('Name', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + 'sort=imdb_rate&sort_type=desc')
    oGui.addFolder(cGuiElement('IMDB', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + 'sort=rate_point&sort_type=desc')
    oGui.addFolder(cGuiElement('Rate', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL + 'sort=view_total&sort_type=desc')
    oGui.addFolder(cGuiElement('View', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', baseURL)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.setEndOfDirectory()


def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    sHtmlContent = cRequestHandler(entryUrl).request()
    pattern = 'Genre</option>.*?</div>'
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, pattern)

    if  isMatch:
        pattern = 'value="([^"]+)">([^<]+)'
        isMatch, aResult = cParser.parse(sContainer, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    for sID, sName in sorted(aResult, key=lambda k: k[1]):
        params.setParam('sUrl', entryUrl + 'category=' + sID + '&country=&sort=&key=&sort_type=desc')
        oGui.addFolder(cGuiElement(sName.strip(), SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    oRequest = cRequestHandler(entryUrl + '&page=' + str(iPage) if iPage > 0 else entryUrl, ignoreErrors=(sGui is not False))
    oRequest.addHeaderEntry('Referer', 'https://hdfilme.cc/')
    oRequest.addHeaderEntry('Upgrade-Insecure-Requests', '1')
    oRequest.addParameters('load', 'full-page')
    oRequest.setRequestType(1)
    
    sHtmlContent = oRequest.request()
    pattern = '<ul[^>]class="products row">(.*?)</ul>'
    isMatch, sContainer = cParser.parseSingleResult(sHtmlContent, pattern)

    if isMatch:
        pattern = '<div class="box-product clearfix" data-popover.*?href="([^"]+).*?data-src="([^"]+).*?title=".*?">([^<]+)'
        isMatch, aResult = cParser.parse(sContainer, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    cf = cRequestHandler.createUrl(entryUrl, oRequest)
    total = len(aResult)
    for sUrl, sThumbnail, sName in aResult:
        sName = sName.replace(' stream', '')
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        sThumbnail = sThumbnail.replace('_thumb', '') + cf
        isMatch, sYear = cParser.parse(sName, "(.*?)\((\d*)\)")
        for name, year in sYear:
            sName = name
            sYear = year
            break

        isTvshow = True if 'staffel' in sUrl or 'staffel' in sName else False

        if 'sort=year&sort_type=desc' in entryUrl and not isTvshow:
            sName += ' (' + str(sYear) + ')'
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showEpisodes' if isTvshow else 'showHosters')
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        if sYear:
            oGuiElement.setYear(sYear)
        params.setParam('entryUrl', sUrl)
        params.setParam('sName', sName)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        sPageNr = int(params.getValue('page'))
        if sPageNr == 0:
            sPageNr = 2
        else:
            sPageNr += 1
        params.setParam('page', int(sPageNr))
        params.setParam('sUrl', entryUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if URL_SHOWS in entryUrl else 'movies')
        oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sUrl = cParser.urlEncode(params.getValue('entryUrl'),':|/') + '/folge-1'
    sThumbnail = params.getValue('sThumbnail')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'data-episode-id="([\d]+).*?folge.*?([\d]+)'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    pattern = 'data-movie-id="([\d]+)'
    isMatch, sID = cParser.parse(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    
    total = len(aResult)
    for eID, eNr in aResult:
        oGuiElement = cGuiElement('Folge ' + eNr , SITE_IDENTIFIER, "showHosterserie")
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        params.setParam('eID', eID)
        params.setParam('sID', sID[0])
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showHosterserie():
    hosters = []
    eID = ParameterHandler().getValue('eID')
    sID = ParameterHandler().getValue('sID')
    rUrl = ParameterHandler().getValue('entryUrl')
    oRequest = cRequestHandler(str(URL_MAIN + '/movie/load-stream/' + sID + '/' + eID + '?server=2'))
    oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequest.addHeaderEntry('Referer', rUrl)
    sHtmlContent = oRequest.request()
    pattern = 'label":"([^"]+).*?file":"([^"]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    for sQualy, sUrl in aResult:
        hoster = {'link': sUrl, 'name': sQualy + sUrl}
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def showHosters():
    hosters = []
    sUrl = cParser.urlEncode(ParameterHandler().getValue('entryUrl'),':|/') + '/deutsch'
    rUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'data-movie-id="(.*?)"[\s\S]*?data-episode-id="(.*?)"' #'data-episode-id="([^"]+).*?load[^>] "([^"]+)"'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
        for sMID, sEID in aResult:
            oRequest = cRequestHandler(str(URL_MAIN + '/movie/load-stream/' + sMID +'/'+ sEID + '?server=2'))
            oRequest.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequest.addHeaderEntry('Referer', rUrl)
            sHtmlContent = oRequest.request()
            pattern = 'label":"([^"]+).*?file":"([^"]+)'
            isMatch, aResult = cParser().parse(sHtmlContent, pattern)
            for sQualy, sUrl in aResult:
                hoster = {'link': sUrl, 'name': sQualy}
                hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    sUrl = sUrl + '|' + 'Origin=https%3A%2F%2Fhdfilme.cc%2F&Accept-Language=de-de,de;q=0.8,en-us;q=0.5,en;q=0.3&Accept-Encoding=gzip&Referer=https%3A%2F%2Fhdfilme.cc%2F'
    return [{'streamUrl': sUrl, 'resolved': True}]


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_SEARCH % sSearchText, oGui, sSearchText)
