Kodi Tips & Linklist
========================================
* Kodi wird gerne modifiziert was man dann "Build" nennt. Ich habe diverse bekannte Builds getestet & am ende mir ein eigenen erstellt der die besten Addons für den Deutschsprachigen Raum mitbringt. 

Die Addons sind in meinem Repo ([repository.myrepo-1.0.2.zip](https://dbiesecke.github.io/repo/repository.myrepo/repository.myrepo-1.0.2.zip) ) & auf dem [HiDrive](https://my.hidrive.com/share/w4jo.f9fzu) Laufwerk gespeichert.



-------------------



| Packages                      | DL                                                                                                |  
|-------------------------------|---------------------------------------------------------------------------------------------------|
| repository.myrepo-1.0.2.zip | [repository.myrepo.zip](http://dbiesecke.github.io/repo/repository.myrepo/repository.myrepo-1.0.2.zip)      |


## Installation
* LibreElec Image runterladen ( only for Raspi4 !) - [Hidrive-LIBRE-backup.img.gz](https://my.hidrive.com/lnk/EEBpFRYj) & diese per dd auf die SD Card schreiben: `zcat -f ./LIBRE-backup.img.gz | dd of=/dev/sdc `

* Raspi starten & Netzwerk einrichten. Bitte sicherstellen das ein NTP eingetragen ist & IP Addresse statisch vergeben. DNS wenn am besten direkt auf 8.8.8.8 einstellen. ( Um DNS Blockade bsp von Vodafone zu umgehen)

* Aus meinem Repo bitte "EZMaintenance+" Installieren

![BRGQr5m.png](https://i.imgur.com/BRGQr5m.png) 

![TSoqee7.png](https://i.imgur.com/TSoqee7.png)


* Ihr könnt mit dem Tool unter dem Menüpunkt "Wizard" auf meine unterschiedlichen Builds zugreifen & diese installieren.

![o2KyV6E.jpg](https://i.imgur.com/o2KyV6E.jpg)




## Plugins
--------------------------------


| Name                        	| Infos                                                                      | 
|----------------------------	|--------------------------------------------------------------------------- |
| zappntv                       | IPTV DE & Mediathekk (UDP Proxy, DRM Plugin, DRM installer)                   | 
| tvone, tvone11, ..            | IPTV, Diverse Sprache & Sky enthalten.                                     | 
| DDL.me,HD-Filme.net           | Link Provider für Movies/Serien                                            | 
| XStream                       | Sammlung mit weiteren Seiten (Animestream24,doku-stream,kinox,kinox,..)    | 
| 7Tv,TVNOW                     | Mediatheken                                                                |













OUTDATED!!!!
==========================



Wizards - 
------------------------
Depends:  Kodi 18.1++ 

![](https://i.imgur.com/3yzdHpS.png)

* Ghost ist der wohl beste Kodi build der mir untergekommen ist -  [ghost-repo.de](http://ghost-repo.de/)

* Für leistungsschwache maschinen wie FireTV stick, rate ich eher zum Sunrise-Build - dieser hat eine wesentlich schlichtere GUI





![sunrise-install-sunrise-wizard.gif](https://dbiesecke.github.io/images/sunrise-install-sunrise-wizard.gif)


                                                 





## Installation
======================================================
1. Installiert als erstes mein Repo ( [repository.myrepo.zip](/plugin.program.sunrisewizard/plugin.program.sunrisewizard-1.04.zip) )
![TPaRZRQ.png](https://i.imgur.com/TPaRZRQ.png) 

2. Laded aus dem Repo bitte unter Programme den "Ghost Wizzard"
 ![woX9viH.png](https://i.imgur.com/woX9viH.png)

3. Es gibt 2x verschiedene Installer, welchen ihr genau nehmt ist euch überlassen. Der aktuell letzte build ist ist `Shin 2.1.6`  ![wFpyshG.png](https://i.imgur.com/wFpyshG.png)





## 3rd-party / hoster
=====================================================

* Viele Streamanbieter/Programme (trakt) erwarten ein Pairing im Browser damit man dort streamen/editieren kann. Das Program `script.SGKPAIR` erleichtert dabei die Arbeit erheblich

![lZqgNyX.png](https://i.imgur.com/lZqgNyX.png)


| Packages                                                              | Plugin                                                                                                |  
|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [linksnappy.com](https://linksnappy.com/?ref=306077)                  | script.SGKPAIR                                                                                                  |
| [www.flashx.tv](https://www.flashx.tv/?op=my_account)                 | urlresolver                                                                                                   |





Kodi Video Plugins/Addons
---------------------------


    
  * [IPTV Simple PVR-addon](http://www.kodinerds.net/index.php/Thread/26042-IPTV-Simple-PVR-addon-mit-XMLTV-EPG/?pageNo=1)
    - Bringt euch TV mit EPG direkt auf's XBMC, mit über 40 deutschen TV Sendern ( Pro7/ORF/ARD/etc) !   [Mehr Infos...](http://www.kodinerds.net/index.php/Thread/26042-IPTV-Simple-PVR-addon-mit-XMLTV-EPG/?pageNo=1)



  * [My Music Videos](http://ftp.gnome.org/mirror/addons.superrepo.org/v5/addons/plugin.video.my_music_tv/plugin.video.my_music_tv-1.0.6.zip)
    * Es lassen sich per XML diverse Music Video Channels erstellen, bsp:
    
      <channel thumb="THUMB_URL" shuffled="no" unwatched="yes">
	  <entry title="VEVO: Top20 Today" type="vevo:charts" limit="20" cache="1" value="all:MostViewedToday" />
      </channel>
    
    
    
    
German Repository
---------------------

  * [Addonscriptorde-beta](https://code.google.com/p/addonscriptorde-beta-repo/downloads/detail?name=repository.addonscriptorde-beta.zip&can=2&q=) | [On Github](https://github.com/AddonScriptorDE?tab=repositories)
    - Wohl der aktivste Deutsche Addon Entwickler, der neue maßstäbe in sachen qualität in der deutschen Community gesetzt hat, Hut ab!
    
  * [KODInerds](http://www.kodinerds.net/index.php/Thread/30541-KODInerds-Repository/)
    - DIE Deutsche Kodi Community!
    
  * [Membran](http://code.google.com/p/membrane-xbmc-repo/downloads/detail?name=repository.membrane.xbmc-plugins.zip&can=2&q=)
    - Entwickler der ersten Stunden von ehemals XBMC. AddonScriptorDE hat diverse Addons die sich überschneiden.
    
    
Int. Repository
-------------------

  * [lunatixz Repository](https://github.com/Lunatixz/XBMC_Addons/blob/master/zips/repository.lunatixz/repository.lunatixz-1.0.zip?raw=true)
    - Enthält intressante Plugins wie "PseudoLibary" & Pseudo TV Live

  * [xbmc-hub-repo](https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/)
    - Offizielles Repo vom Navi-X, siehe auch [naviextreme.com](http://www.navixtreme.com/)
    
    
Externe Tools
---------------

  * [xbmc-mylibary](https://code.google.com/p/xbmc-mylibrary/)
    - Erstellt aus Addon-Einträgen strm-datein. Durchforstet per XML von mir ausgesuchte Plugins & wendet diverse Regex/Scraper auf die datein an woraus "Kodi-Kompatibele" Ordner & strm-Dateien werden.
    
    
    
    
OLD - Outdated Stuff
----------------------------

  * [Anime/Serien Addon Sammlung - animeanime0.6a](https://github.com/dbiesecke/plugin.video.animeanime/releases/download/0.6a/plugin.video.animeanime-v0.6a.zip)
    - Mein Fork für kompatibilität mit XBMC-MyLibary, Zugriff auf die neusten Deutschen Fansubs & Retail Animes 
    - Benötigt Plugins:      [script.module.crypto](https://github.com/moneymaker365/xbmc-xbmcplus-plugins/blob/master/download/script.module.cryptopy/script.module.cryptopy-1.2.6.zip?raw=true) | [requests](http://mirrors.xbmc.org/addons/frodo/script.module.requests/script.module.requests-2.3.0.zip)
    - Folgende Plugins erweitern das Addon um automatische mirrorsuche: [Anime-tube.tv](https://www.dropbox.com/s/f8p90m5dvrrqkxi/plugin.video.animetube.1.2.5.zip?dl=1)  | [genx-anime](https://www.dropbox.com/s/ofvmajxr9zgtif8/plugin.video.genxanime.1.3.1.zip?dl=1) [clipfish](https://db.tt/a3IkHLe9)



![sunrise-intro.gif](https://dbiesecke.github.io/images/sunrise-intro.gif)


| Packages                      | DL                                                                                                |  
|-------------------------------|---------------------------------------------------------------------------------------------------|
| [Latest Ghost repo/installer](http://ghost-repo.de/)   | [repository.Ghost.zip](http://ghost-repo.de/repository.Ghost.zip)  / [plugin.program.Ghost.zip](http://ghost-repo.de/plugin.program.Ghost.zip)      |

