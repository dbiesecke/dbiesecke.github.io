My Wiki
- - - - - - 
* Notes to myself, all writen in clear MarkDown ;)



Lets Encrypt rockt!
------------------------------------- 

Als ich einen neuen webserver/reverse-proxy brauchte bin ich auf [caddy](https://caddyserver.com/download) gestoßen.
Allein die die features wie Git,Markdown & search plugins machen ihn ja schon zu na wucht. Aber seit kurzem unterstützt 
er auch ne lets-encrypt integration. Das heißt für euch OHNE config

| Tools/Libs                    | Lang | DL                                              | My-opinion                                                |
|-------------------------------|------|-------------------------------------------------|-----------------------------------------------------------|
| Caddy - HTTP Server           | GO   | [LINK](https://caddyserver.com/download)        | fast Webserver and will auto-generate a SSL cert for you! |
| LEGO - Go Lets Encrypt Client | GO   | [LINK](https://github.com/xenolf/lego/releases) | Easy to use Client to generate Certs                      |
|                               |      |                                                 |                                                           |




continuous integrations über wercker
----------------------------------------

[![wercker status](https://app.wercker.com/status/0e32abc3e5a861cc6d825b12817d7f4a/m "wercker status")](https://app.wercker.com/project/bykey/0e32abc3e5a861cc6d825b12817d7f4a)

![Wercker](http://i.imgur.com/wqCK5eW.jpg) 


[Wercker](https://wercker.com/) ist ein sehr flexibles aber auch einfach zu implementierendes  "continuous integrations system". Aktuell erstellt es von meinem meiner Perl Packete ein Docker Container & transferiert ihn über scp auf meinen Server.


![Wercker](http://i.imgur.com/rnGI1Ki.jpg)




Aptly CheatSheet verlinkt
----------------------------------
Meine kurz anleitung für [aptly](/#!https://gist.githubusercontent.com/dbiesecke/5ecd3d5d2de50bcd30aa/raw/README.md) habe ich hinzugefügt.
Dies macht es einem einfach sein eignes deb Repository zu pflegen. 



Gist notes hinzugefügt
----------------------------------
Ich habe kleines script geschrieben um weitere Notes aus Gist zu importieren.
Den src findet ihr hier: [my-gist-info.pl](http://dbiesecke.github.io/tools/my-gist-info.pl)


Added patch to hurik/MangaDownloader
----------------------------------
* Added top DE sites to [hurik/MangaDownloader](https://github.com/hurik/MangaDownloader)

![](http://i.imgur.com/ovu8bwA.jpg) 


Kodi
----------------------------------
* Config für [IPTV Simple PVR](/#!repo/pvr.iptvsimple/README.md) mit aktuellen EPG hinzugefügt
* [IPTVExtra](/#!my/kodi/iptvextra.md) als alternative zu Simple PVR ( mehrer Sprachen etc)


[![](/repo/repository.iptvxtra/icon.png)](/#!my/kodi/iptvextra.md)
[![](/repo/pvr.iptvsimple/icon.png)](/#!repo/pvr.iptvsimple/README.md)
[![](/repo/repository.xstream/icon.png)](/repo/repository.xstream/repository.xstream-1.0.5.zip)
[![](/repo/repository.addonscriptorde-beta/icon.png)](/repo/repository.addonscriptorde-beta/repository.addonscriptorde-beta-1.0.1.zip) 



Java2Binary on *nix
----------------------------------
Ich schweif heute mal bischen von meinen Üblichen Themen ab, aber das auch nur weil ich auf 2x Intressante Projecte gestoßen bin.
Ich hatte als ziel nen Java Source (drFTPD) in ne portable binary zu gießen, was je nach ran gehnsweise ganz gut funktioniert.

Vorweg: Es würde den projecten nicht gerecht wenn man die "frameworks/tools" nur für´s reihne builden verwendet, vorallem IKVM 
baut eine solide Mono Grundlage für weitere entwicklungen, wobei robovm mono unabhängige binarys baut.

[ikvm](http://www.ikvm.net/) und [robovm](http://www.robovm.org/)


