Import Kodi Plugins to your Libary!
========================================
.... oder, "wie importiert man mehre Tausend Serien-Streams in die Kodi Medien Bibliothek?" 

Ich hatte mir schon seit einer geraumen Zeit vorgenommen, diverse Serien bei mir durch Stabile Online Streams 
zu ersetzen. Wer brauch schon 64GB an McGuyver folgen auf der HDD, nur weil er mal 1-2 folgen pro Monat guckt? Da wir in Deutschland eine verdammt große Serienjunkies Community haben & mit [Burning-Series](https://www.burning-seri.es/) auch noch eine Programmier freundliche API, war es nicht sonderlich schwer dies Umzusetzen.


Konzept
-------------------------


![](http://yuml.me/diagram/scruffy/class/[USER|-Start-Playback-Episode]-1>[myhttp-server|-strm-file],[myhttp-server|-strm-file]<>-2>[plugin.video],[plugin.video]<>-3>[burning-series|-resolve-URL],[plugin.video]+-4>[USER|-Start-Playback-Episode])


Install
-----------

1. Alle benötigten (Kodi/XBMC) Plugins:
  * [script.module.crypto](https://github.com/moneymaker365/xbmc-xbmcplus-plugins/blob/master/download/script.module.cryptopy/script.module.cryptopy-1.2.6.zip?raw=true)
    - Libary  für das Burning Series/animeanime Kodi Plugin
  * [plugin.video.animeanime-v0.6a](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/plugin.video.animeanime-v0.6a.zip)
    - Mein Fork für kompatibilität mit XBMC-MyLibary, Zugriff auf die neusten Deutschen Fansubs & Retail Animes 
    - Anlaufstelle für alle STRM files, versucht ein Mirror zu finden, falls Stream nicht verfügbar ist.
      genx-anime.org - burning-seri.es - tavernakoma.net anime-world24.net - anime-tube.tv - de.anisearch.com animiru.org - proxer.me
  * [Amazon Prime Instant Video Plugin) - download über Addonscriptorde-Repo](https://code.google.com/p/addonscriptorde-beta-repo/downloads/detail?name=repository.addonscriptorde-beta.zip&can=2&q=)
    - Wird für diverse wichtige Maijor serien benötigt - wird eingesetzt aufgrund Qualität der streams etc.

2. Downloaden des gewünschten Serien Packet's & entpackt es in einen Ordner den ihr per XBMC überwacht.
  * [serien-small-strm-db.zip](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/serien-small-strm-db.zip) 
    - Beinhaltet 29 der meistgeschauten serien in Deutschland (Simpsons,Big.Bang,2.Broke.Grils.....)
  * [anime-strm-db.tar.gz](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/anime-strm-db.tar.gz)
    - Beinhaltet 500 Anime Serien, alle mind. mit Deutschen untertiteln!

3. Startet einen neuen Content scan & schwup habt ihr eine gut gefüllte Libary ;)

PS: Ich kamm mit meinem Anime Addon auf knapp 1200 Serien, 12k Episoden ;)




Backend - Technischer Hintergrund
-------------------------

Kern des Konstrukt ist ein [Modifiziertes Addon](https://github.com/dbiesecke/plugin.video.animeanime), [xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/) und die Serien Datenbank [Burning-Series-API](https://www.burning-seri.es/) [API-HOWTO](https://gist.github.com/Bouni/8323ee9606fb502c8e17).

Auf meinem Server wird in regelmäßigen Abständen das komplette [Addon](https://github.com/dbiesecke/plugin.video.animeanime) von [xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/) durchforstet & von mir hinterlegte Regex angewandt. [Xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/) wird daraufhin "Kodi-Kompatibele" Ordner & strm-Dateien erstellen. 

Die eigentlichen "Watch/Dowload" URL's werden immer beim  Playback einer Episode von  burning-seri.es per API geholt & wiedergegeben.
Das sorgt für die benötigte ausfallsicherheit & flexibilität, da burning-seri.es mehrere mirrors pro folge zur verfügung stellt.

Der "Trick" der strm dateien ist, sie Ihre "Watch-URL/Mirror" dynamisch per addon beziehen. Somit müssen die strm dateien nur 
1x erstellt werden & um den rest kümmert sich das das addon ;)

![](http://yuml.me/eba5d2c5 "UML")



Notes
----------  

  .... follow's

