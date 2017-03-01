Diverse Linux OneLiner
---------------------------------


* Install Update Parallel
------------------------
# `(wget pi.dk/3 -qO - ||  curl pi.dk/3/) | bash`



Install kali tools/Menu on ubuntu
--------------------------------
# git clone https://github.com/LionSec/katoolin.git  && cp katoolin/katoolin.py /usr/bin/katoolin && chmod +x  /usr/bin/katoolin && katoolin


Install Conky-Manager
---------------------
* ![Desktop](http://storage2.static.itmages.com/i/16/0828/h_1472385934_3730740_62ae560e3f.png)

* FOr Thems Package, look at : [teejeetech.in](http://www.teejeetech.in/p/conky-manager.html)


            $ sudo add-apt-repository ppa:teejee2008/ppa     
            $ apt-get update && apt-get install conky-manager
            

| Name                       	| DL 	| INFO 	|
|----------------------------	|----	|------	|
| dbiesecke Themes              	|[dbiesecke.cmtp.7z](http://dbiesecke.github.io/dbiesecke.cmtp.7z)    				| My Conky workspace |
| Conky default Themes              |[default-themes-extra-1.cmtp.7z](https://github.com/dbiesecke/dbiesecke.github.io/blob/master/default-themes-extra-1.cmtp.7z?raw=true)    				| Conky Theme Package |






idok - Kodi CLI Player
----------------------------
* Can easy installed with `bash <(wget https://goo.gl/imm9jP -qO -)`
* Now a example idok config `~/.config/idok/idok.conf`


    target = 127.0.0.1
    targetport = 8080
    login = kodi
    
    password = kodi
    ssh = false
    release-check = false
    

rcm - dotfile managment
-------------------------------
* More infos on [github](https://github.com/thoughtbot/rcm)
* If done, make Install script with: `$ env RCRC=/dev/null rcup -B 0 -g > ~/.dotfiles/install.sh`


    wget https://thoughtbot.github.io/rcm/debs/rcm_1.3.0-1_all.deb
    sha=$(sha256sum rcm_1.3.0-1_all.deb | cut -f1 -d' ')
    [ "$sha" = "2e95bbc23da4a0b995ec4757e0920197f4c92357214a65fedaf24274cda6806d" ] && \
    sudo dpkg -i rcm_1.3.0-1_all.deb



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



App::Every
---------------------------------
Makes a cron entry with 2x simple parameters.

* Alias: `alias cron-every='curl -sk 'https://raw.githubusercontent.com/iarna/App-Every/master/packed/every' | perl -X - -n  -l'`

*  Example:

    `% cron-every 3 hours ls`


        PATH=/home/foilo/cappucino/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/foilo/.rvm/bin
        LOCKFILE=/tmp/every_lock_b8d65f1a8f00500bbda75fc44a4d5f88
        SHELL=/bin/zsh
        54 */3 * * * [ ! -f $LOCKFILE -o ! -d /proc/`[ -f $LOCKFILE ] && cat $LOCKFILE` ] && ( echo $$ > $LOCKFILE ; cd "/home/foilo";  ls  ; rm $LOCKFILE )


Debian GRML scripts
---------------------------------

            wget -qO- http://deb.grml.org/repo-key.asc | sudo apt-key add --    
            sudo echo   'deb     http://deb.grml.org/ grml-testing main' > /etc/apt/sources.list.d/grml.list
            sudo apt-get update 

Install some usefull tools
---------------------------------

            sudo apt-get install grml-tips grml-crypt grml-network grml-paste grml-shlib grml-tips grml-quickconfig grml-scripts
            
Install ZSH
---------------------------------

            wget -qO- .zshrc http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc


Install gvm and go
----------------------------------

            $ sudo apt-get install curl git mercurial make binutils bison gcc build-essential
            % bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
            % source ~/.gvm/scripts/gvm 
            % gvm install go1.4 -B
            % gvm use go1.4
            % export GOROOT_BOOTSTRAP=$GOROOT
            % gvm install go1.5


Monodevelop Latest
---------------------------------

            sudo add-apt-repository ppa:keks9n/monodevelop-latest
            
Scribes
---------------------------------

            sudo add-apt-repository ppa:mystilleef/scribes-daily
