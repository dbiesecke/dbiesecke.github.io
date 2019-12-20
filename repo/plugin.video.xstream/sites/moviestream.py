# -*- coding: utf-8 -*-
from resources.lib import logger
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'moviestream'
SITE_NAME = 'MovieStream'
SITE_ICON = 'moviestream.png'

URL_MAIN = 'https://movie-stream.eu/'
URL_FILME = 'https://movie-stream.eu/secure/titles?type=movie&onlyStreamable=true'
URL_SERIE = 'https://movie-stream.eu/secure/titles?type=series&onlyStreamable=true'
URL_HOSTER = URL_MAIN + 'secure/titles/%s?titleId=%s'
URL_SEARCH = URL_MAIN + 'secure/search/%s?type=&limit=20'

URL_GENRES_LIST = {'Drama' : 'drama', 'Action' : 'action', 'Thriller' : 'thriller', 'Science Fiction' : 'science fiction', 'Horror' : 'horror', 'Mystery' : 'mystery', 'Komoedie' : 'komoedie', 'Liebesfilm' : 'liebesfilm'}
URL_GENRES_FILME = 'https://movie-stream.eu/secure/titles?type=movie&genre=%s&onlyStreamable=true'
URL_GENRES_SERIE = 'https://movie-stream.eu/secure/titles?type=series&genre=%s'


def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('page', (1))
    params.setParam('sUrl', URL_FILME)
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('Genre', URL_GENRES_FILME)
    oGui.addFolder(cGuiElement('Film Genre', SITE_IDENTIFIER, 'showGenre'), params)
    params.setParam('sUrl', URL_SERIE)
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('Genre', URL_GENRES_SERIE)
    oGui.addFolder(cGuiElement('Serien Genre', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()


def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    Genre = params.getValue('Genre')
    for key in sorted(URL_GENRES_LIST):
        params = ParameterHandler()
        params.setParam('sUrl', (Genre % URL_GENRES_LIST[key]))
        oGui.addFolder(cGuiElement(key, SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    iPage = int(params.getValue('page'))
    if iPage > 0:
        entryUrl = entryUrl + ('&' if '?' in entryUrl else '?') + 'page=' + str(iPage)
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    oRequest.addHeaderEntry('Referer', params.getValue('sUrl'))
    sHtmlContent = oRequest.request()
    pattern = '"id":([\d]+).*?"name":"([^"]+).*?year":([\d]+).*?description":"([^"]+).*?poster":"([^"]+).*?backdrop":"([^"]+)","runtime":([\d]+).*?is_series":([^"]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sUrl, sName, sYear, sDesc, sThumbnail, sFanart, runtime, isserie in aResult:
        isTvshow = True if "true" in isserie else False
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setYear(sYear)
        oGuiElement.setDescription(sDesc)
        oGuiElement.addItemValue('duration', int(runtime) * 60)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('entryUrl', URL_HOSTER % (sUrl, sUrl))
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        isMatch, strPage = cParser().parseSingleResult(sHtmlContent, 'last_page":([\d]+)')
        if isMatch:
            if float(int(strPage)) > iPage:
                params.setParam('page', (iPage + 1))
                oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if 'true' in isserie else 'movies')
        oGui.setEndOfDirectory()


def showSeasons():
    oGui = cGui()
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    sTVShowTitle = params.getValue('sName')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'number":([\d]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    isDesc, sDesc = cParser.parse(sHtmlContent, 'description","content":"([^"]+)')
    total = len(aResult)
    for sSeasonNr in aResult:
        oGuiElement = cGuiElement('Staffel ' + sSeasonNr, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        if isDesc:
            oGuiElement.setDescription(sDesc[0])
        params.setParam('sSeasonNr', sUrl + '&seasonNumber=' + sSeasonNr)
        oGui.addFolder(oGuiElement, params, True, total)
    oGui.setView('seasons')
    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    params = ParameterHandler()
    sSeasonNr = params.getValue('sSeasonNr')
    sHtmlContent = cRequestHandler(sSeasonNr).request()
    pattern = 'id":\d+,"name":"([^"]+)","description":"([^"]+).*?poster":"([^"]+).*?episode_number":([\d]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)

    if not isMatch:
        oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sName, sDesc, sThumbnail, sEpisodeNr in aResult:
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('sEpisodeNr')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        oGuiElement.setDescription(sDesc)
        params.setParam('entryUrl', sSeasonNr + '&episodeNumber=' + sEpisodeNr)
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showSearchEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    oRequest.addHeaderEntry('Referer', params.getValue('sUrl'))
    sHtmlContent = oRequest.request()
    pattern = '"id":([^,]+),"name":"([^"]+)","year":([\d,]+),"description":"([^"]+)","poster":"([^"]+)","is_series":([^,]+).*?type":"title'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)

    if not isMatch:
        if not sGui: oGui.showInfo('xStream', 'Es wurde kein Eintrag gefunden')
        return

    total = len(aResult)
    for sUrl, sName, sYear, sDesc, sThumbnail, isserie in aResult:
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        isTvshow = True if "true" in isserie else False
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sThumbnail)
        oGuiElement.setYear(sYear)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('entryUrl', URL_HOSTER % (sUrl, sUrl))
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        isMatch, strPage = cParser().parseSingleResult(sHtmlContent, 'last_page":([\d]+)')
        if isMatch:
            if float(int(strPage)) > iPage:
                params.setParam('page', (iPage + 1))
                oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if 'true' in isserie else 'movies')
        oGui.setEndOfDirectory()


def showHosters():
    sUrl = ParameterHandler().getValue('entryUrl')
    sHtmlContent = cRequestHandler(sUrl).request()
    pattern = 'id":\d+,"name":"([^"]+)","thumbnail.*?url":"([^"]+)'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    hosters = []
    if isMatch:
        for sName, sUrl in aResult:
            if not 'youtube' in sUrl:
                hoster = {'link': sUrl, 'name': sName}
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
    showSearchEntries(URL_SEARCH % sSearchText, oGui, sSearchText)
