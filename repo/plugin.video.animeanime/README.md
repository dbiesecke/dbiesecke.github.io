# plugin.video.animeanime

Import Kodi Plugins to your Libary!
========================================

.... oder, "wie importiert man mehre Tausend Serien-Streams in die Kodi Medien Bibliothek?" 

![](http://i.imgur.com/v2pny4q.jpg)


Konzept
-------------------------

![](http://yuml.me/diagram/scruffy/class/[USER|-Start-Playback-Episode]-1>[myhttp-server|-strm-file],[myhttp-server|-strm-file]<>-2>[plugin.video],[plugin.video]<>-3>[burning-series|-resolve-URL],[plugin.video]+-4>[USER|-Start-Playback-Episode])


Main Plugin
-----------

  * Main Plugin, resolvt die URL's aus den Datein & startet passenden Stream/Plugin


| Name                       	| DL 	| INFO 	| BETA?	|
|----------------------------	|----	|------	|-----	|
| Main Plugin & Repo         	|[plugin.video.animeanime-1.0.2.zip](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/v1.0.02/plugin.video.animeanime-1.0.2.zip)    	|      	[github](https://github.com/dbiesecke/plugin.video.animeanime/releases)												|  YES!	|



Burning Files
-----------

  * Dies sind die strm Dateien, diesen auf euren Kodi client packen & scraper konfigurieren 

| Burning Series Files        	| DL 	| NOTE 	| Anime?|
|----------------------------	|----	|------	|-----	|
| All Serien     	|[burn-db.zip](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/v1.0.02/burn-db.zip)    	|      		|  YES!	|
| Only Anime	   	|[anime-strm-db.tar.gz](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/anime-strm-db.tar.gz)    	|      		|  YES!	|
| Only some Selected  	|[serien-small-strm.zip](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/serien-small-strm-db.zip)    	| (Simpsons,Big.Bang,2.Broke.Grils.....)|  NO?	|



Install
-----------

1. Installiert die aktuelle Version von [plugin.video.animeanime.zip](#Main_Plugin)
  * [script.module.cryptopy-1.2.6.zip](https://github.com/moneymaker365/xbmc-xbmcplus-plugins/blob/master/download/script.module.cryptopy/script.module.cryptopy-1.2.6.zip?raw=true)
    - Libary  für das Burning Series/animeanime Kodi Plugin, sollte bei den meisten bereits installiert sein.
    

2. Downloaden des gewünschten Serien Packet's & entpackt es in einen Ordner den ihr per Kodi überwacht.
  * [serien-small-strm-db.zip](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/serien-small-strm-db.zip) 
    - Beinhaltet 29 der meistgeschauten serien in Deutschland (Simpsons,Big.Bang,2.Broke.Grils.....)
  * [anime-strm-db.tar.gz](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/anime-strm-db.tar.gz)
    - Beinhaltet 500 Anime Serien, alle mind. mit Deutschen untertiteln!

3. Startet einen neuen Content scan & schwup habt ihr eine gut gefüllte Libary ;)




Backend - Technischer Hintergrund
-------------------------

![](http://yuml.me/eba5d2c5 "UML")

Ich hatte mir schon seit einer geraumen Zeit vorgenommen, diverse Serien bei mir durch Stabile Online Streams 
zu ersetzen. Wer brauch schon 64GB an McGuyver folgen auf der HDD, nur weil er mal 1-2 folgen pro Monat guckt? Da wir in Deutschland eine verdammt große Serienjunkies Community haben & mit [Burning-Series](https://www.burning-seri.es/) auch noch eine Programmier freundliche API, war es nicht sonderlich schwer dies Umzusetzen.

Kern des Konstrukt ist ein [Modifiziertes Addon](https://github.com/dbiesecke/plugin.video.animeanime), [xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/) und die Serien Datenbank [Burning-Series-API](https://www.burning-seri.es/) [API-HOWTO](https://gist.github.com/Bouni/8323ee9606fb502c8e17).

Auf meinem Server wird in regelmäßigen Abständen das komplette [Addon](https://github.com/dbiesecke/plugin.video.animeanime) von [xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/) durchforstet & von mir hinterlegte Regex angewandt. [Xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/) wird daraufhin "Kodi-Kompatibele" Ordner & strm-Dateien erstellen. 

Die eigentlichen "Watch/Dowload" URL's werden immer beim  Playback einer Episode von  burning-seri.es per API geholt & wiedergegeben.
Das sorgt für die benötigte ausfallsicherheit & flexibilität, da burning-seri.es mehrere mirrors pro folge zur verfügung stellt.

Der "Trick" der strm dateien ist, sie Ihre "Watch-URL/Mirror" dynamisch per addon beziehen. Somit müssen die strm dateien nur 
1x erstellt werden & um den rest kümmert sich das das addon ;)




Notes
----------  

  .... follow's

