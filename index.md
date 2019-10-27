My Wiki
- - - - - - 
* Notes to myself, all writen in clear MarkDown ;)


Storage Tips & Tricks 
==========================================================
* ... or  "How to get 100TB++ for free from google"
* Die meisten Tools basieren auf dem sehr guten "rclone", dieser kommt nun auch mit WebUI daher
 
![AnkDhuE.png](https://i.imgur.com/AnkDhuE.png)


## Install
------------------------
* Install main binary  `curl https://rclone.org/install.sh | sudo bash`
* Install sprinkle from source: 


    sudo -H python3.6 -mpip install git+https://github.com/mmontuori/sprinkle.git

* Initial sollte man erstmal ein "paar" Service accounts erstellen. Dabei hilft [AutoRclone](https://github.com/xyou365/AutoRclone) & macht es so möglich ganz easy 600 accounts zu erstellen.
 
## Tools
-----------


| Name         | Key #1                                                                             | Tolls     |
|--------------|------------------------------------------------------------------------------------|-----------|
| [uds](https://github.com/stewartmcgown/uds)  |  Unlimited Storage - 0 Byte files on Google Docs   | cli/[gui](https://github.com/stewartmcgown/uds-web)    
| [AutoRclone](https://github.com/xyou365/AutoRclone)   | Get ca. 150TB Space from Google            |  CLI        
|  [sprinkle](https://github.com/mmontuori/sprinkle) |  It presents all the RClone available volumes as a single clustered volume. | CLI/SRV 


## Usage
-----------
* Automount with autofs - [rclone-fstab-mount-helper-script](https://github.com/rclone/rclone/wiki/rclone-fstab-mount-helper-script)
* Example commands


        $ rconsole ls <remote>:<path
        $ rconsole mount <remote>:<path /mnt/temp
        
        


## (Web)UI
---------------------
* Start a Webgui server 


    rclone rcd --rc-web-gui --rc-user admin --rc-pass yeah12ha --rc-addr ":5572" --rc-serve 




## Autostart / Service
-------------------------
* hier ein Ubic script was am ende keine auth verwendet (da http davor geschalten wurde) - `/etc/ubic/service/rclone/rclone`
        
        

    #!/usr/bin/perl -w
    
    use Ubic::Service::SimpleDaemon;
    Ubic::Service::SimpleDaemon->new(
     bin => 'rclone rcd --rc-web-gui --rc-no-auth --rc-addr "127.0.0.1:5572" --rc-serve',
     cwd => "/root",
    );



## Sprinkle
-------------------------

* Ich arbeite aktuell mit 100 (google free) accounts & [sprinkle](https://github.com/mmontuori/sprinkle) . Dieser bringt eine simples cli interface & einen daemon mit. 


        $ sprinkle.py ls /backup
        $ sprinkle.py backup /dir_to_backup
        $ sprinkle.py restore /backup /opt/restore_dir
        
        
![Spr8ANG.png](https://i.imgur.com/Spr8ANG.png)



 


Kodi (New)Sunrise 
--------------------------------
* Mit diesem Kodi build ist es möglich alle aktuellen Serien/Filme zuzugreifen. Dafür wird auf diverse Addons zurückgegriffen.
* [more infos](/my/kodi.md)

![sunrise-intro.gif](https://dbiesecke.github.io/images/sunrise-intro.gif)     

* Use Sunrise Wizard to Easy install all things on fresh kodi (18++)


![sunrise-install-sunrise-wizard.gif](https://dbiesecke.github.io/images/sunrise-install-sunrise-wizard.gif)



Meine änderungen: 
=============

* Auto-Playlist Downloader 
* Features: IPTV (inkl. sky)




GitHub IPTV Search
-----------------------------
* Github macht es möglich:* [Germany Sky extension:m3u](https://github.com/search?l=&o=desc&q=Germany+Sky+extension%3Am3u&ref=advsearch&s=indexed&type=Code&utf8=%E2%9C%93) ["EXTINF" "Bundesliga"  extension:m3u](https://github.com/search?o=desc&q=%22EXTINF%22+%22Bundesliga%22++extension%3Am3u&s=indexed&type=Code&utf8=%E2%9C%93)


| Playlists        DE - Free/PayTV  - Stable                                              	|
|-----------------------------------------------------------------------------------------	|
| [kilirushi-de.m3u](https://github.com/kilirushi/m3u/blob/master/de.m3u)               	|
| [mak-iptv.m3u](https://github.com/mak-iptv/iptv/raw/master/germany.m3u)               	|
| [Server1.m3u](https://github.com/SunriseKodi/TV2.0/blob/master/Deutsch/Server1.m3u)                	|
| [psycotv-1](http://psyco.tv/m3us2/1.m3u)  |
| [psycotv-2](http://psyco.tv/m3us2/2.m3u)  |
| [psycotv-3](http://psyco.tv/m3us2/3.m3u)  |
| [psycotv-4](http://psyco.tv/m3us2/4.m3u)  |
| [psycotv-5](http://psyco.tv/m3us2/5.m3u)  |
 

div-command notes
------------------------------
* nach Markdown convertierte liste von commandlinefu commands


  * [div-notes](commands.md)





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
   
   
   


Install Notes!
-------------------------
* Diverse Tips für neu installation



      # basic dev setup
      sudo apt-get install dkms automake autogen build-essential ca-certificates \
      gcc-5-arm-linux-gnueabi g++-5-arm-linux-gnueabi libc6-dev-armel-cross   gcc-5-arm-linux-gnueabihf g++-5-arm-linux-gnueabihf libc6-dev-armhf-cross gcc-5-aarch64-linux-gnu g++-5-aarch64-linux-gnu libc6-dev-arm64-cross gcc-5-mips-linux-gnu g++-5-mips-linux-gnu libc6-dev-mips-cross gcc-5-mipsel-linux-gnu g++-5-mipsel-linux-gnu libc6-dev-mipsel-cross  gcc-5-mips64-linux-gnuabi64 g++-5-mips64-linux-gnuabi64 libc6-dev-mips64-cross gcc-5-mips64el-linux-gnuabi64 g++-5-mips64el-linux-gnuabi64 libc6-dev-mips64el-cross  gcc-5-multilib g++-5-multilib gcc-mingw-w64 g++-mingw-w64 \
      qmake clang llvm-dev libtool libxml2-dev uuid-dev libssl-dev swig openjdk-8-jdk pkg-config patch make xz-utils cpio wget zip unzip p7zip git mercurial bzr texinfo help2man udo less cpanminus nvi iputils-ping mercurial libreadline-dev chromium-browser byobu aptitude zsh 

   
      # KDE 
      sudo apt-get install monodevelop kdevelop-php kdevelop-pg-qt kdevelop-python kate 
      
      
      #install many things over metabrik
      # for kde-neon change lsb release like:
      #  cp /etc/lsb-release /etc/lsb-release.bak 
      #  sed -r 's/DISTRIB_ID.*/DISTRIB_ID=Ubuntu/g' /etc/lsb-release > /etc/lsb-release
      cpanm --local-lib=~/perl5 local::lib && eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)
      cpanm -nf Metabrik Metabrik::Repository
      $ metabrik.sh
      use brik::tool
      run brik::tool install_all_need_packagesrun
      run brik::tool install www::client
      run brik::tool install file::read
      run brik::tool install file::write
      run brik::tool install file::csv
      run brik::tool install http::proxy
      run brik::tool install remote::ssh2
      run brik::tool install remote::ssh2
      run brik::tool install reuse
      run brik::tool install reload-env
      run brik::tool install file::write
      run brik::tool install file::read
      run brik::tool install client::www
      run brik::tool install api::shodan
      run brik::tool install remote::wmi
      run brik::tool install remote::winexe
      run brik::tool install forensic::volatility

      


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




## continuous integrations über wercker
----------------------------------------

[![wercker status](https://app.wercker.com/status/0e32abc3e5a861cc6d825b12817d7f4a/m "wercker status")](https://app.wercker.com/project/bykey/0e32abc3e5a861cc6d825b12817d7f4a)

![Wercker](http://i.imgur.com/wqCK5eW.jpg) 


[Wercker](https://wercker.com/) ist ein sehr flexibles aber auch einfach zu implementierendes  "continuous integrations system". Aktuell erstellt es von meinem meiner Perl Packete ein Docker Container & transferiert ihn über scp auf meinen Server.


![Wercker](http://i.imgur.com/rnGI1Ki.jpg)




Aptly CheatSheet verlinkt
----------------------------------
Meine kurz anleitung für [aptly](/#!https://gist.githubusercontent.com/dbiesecke/5ecd3d5d2de50bcd30aa/raw/README.md) habe ich hinzugefügt.
Dies macht es einem einfach sein eignes deb Repository zu pflegen. 





Added patch to hurik/MangaDownloader
----------------------------------
* Added top DE sites to [hurik/MangaDownloader](https://github.com/hurik/MangaDownloader)

![](http://i.imgur.com/ovu8bwA.jpg) 




Java2Binary on *nix
----------------------------------
Ich schweif heute mal bischen von meinen Üblichen Themen ab, aber das auch nur weil ich auf 2x Intressante Projecte gestoßen bin.
Ich hatte als ziel nen Java Source (drFTPD) in ne portable binary zu gießen, was je nach ran gehnsweise ganz gut funktioniert.

Vorweg: Es würde den projecten nicht gerecht wenn man die "frameworks/tools" nur für´s reihne builden verwendet, vorallem IKVM 
baut eine solide Mono Grundlage für weitere entwicklungen, wobei robovm mono unabhängige binarys baut.

[ikvm](http://www.ikvm.net/) und [robovm](http://www.robovm.org/)


