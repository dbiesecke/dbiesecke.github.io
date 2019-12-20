# -*- coding: utf-8 -*-
import xbmc
from resources.lib import common
from resources.lib.handler.ParameterHandler import ParameterHandler


def info(sInfo):
    __writeLog(sInfo, cLogLevel=xbmc.LOGNOTICE)


def debug(sInfo):
    __writeLog(sInfo, cLogLevel=xbmc.LOGDEBUG)


def error(sInfo):
    __writeLog(sInfo, cLogLevel=xbmc.LOGERROR)


def fatal(sInfo):
    __writeLog(sInfo, cLogLevel=xbmc.LOGFATAL)


def __writeLog(sLog, cLogLevel=xbmc.LOGDEBUG):
    params = ParameterHandler()

    try:
        if isinstance(sLog, unicode):
            sLog = '%s (ENCODED)' % (sLog.encode('utf-8'))

        if params.exist('site'):
            site = params.getValue('site')
            sLog = "\t[%s] -> %s: %s" % (common.addonName, site, sLog)
        else:
            sLog = "\t[%s] %s" % (common.addonName, sLog)

        xbmc.log(sLog, cLogLevel)


    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), cLogLevel)
        except:
            pass
