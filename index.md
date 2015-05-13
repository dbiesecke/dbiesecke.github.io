My Wiki
- - - - - - 

* Notes to myself, all writen in clear MarkDown ;)


Graphite  Docker & collected
------------------------
Graphite easy install:
======================
Source: [docker-graphite-statsd](https://github.com/dbiesecke/docker-graphite-statsd)

        docker run -d \
        --name graphite \
        -e VIRTUAL_HOST="graph.foilo.de" \
        -p 2003:2003 \
        -p 8125:8125/udp \
        dbiesecke/docker-graphite-statsd
  
  
Fill your graphs!
=======================

* ` echo "sample.gauge:9|g" | nc -u -w0 grap.foilo.de 8125`

* Sample event over HTTP: 

      `curl -X POST "http://graphite/events/" 
      -d '{"what": "Event - deploy", "tags": "deploy", 
      "data": "deploy of master branch happened at Fri Jan  3 22:34:41 UTC 2014"}'`


Ext
=========

* [statistik](https://github.com/godmodelabs/statistik) is a nice node lib & cli for first steps.


                $ docker build -t=dbiesecke/statistik https://gist.githubusercontent.com/dbiesecke/53c51e71efcb32ee6e8c/raw/Dockerfile.statistik
                


            # docker   run -i dbiesecke/statistik                                                                                                                                                                                               
          
            Usage: statistik [options] arguments
          
            Options:
        
            -h, --help         output usage information
            -V, --version      output the version number
            -h, --host <host>  StatsD hostname
        
          Configuration:
        
            $ echo "graphite.local:8125" > ~/.statistik
            currently saved host: graph.foilo.de:8125
        
          Examples:
        
            $ statistik increment visits
            $ statistik timing load 30 0.5
            $ statistik -h graphite.local:8125 gauge mem-usage 12




More infos
==========
* [Blog-digitalocean](https://www.digitalocean.com/community/tutorials/how-to-configure-statsd-to-collect-arbitrary-stats-for-graphite-on-ubuntu-14-04)

Dashing
============
* [Plugin](https://gist.github.com/Ulrhol/5088efcc94de2fecad5e)
* [Plugin-Simple](https://gist.github.com/joerayme/5934555)



Startup / Persistence
------------------------
App::Every
================
Makes a cron entry with 2x simple parameters.

* Alias: `alias cron-every='curl -sk 'https://raw.githubusercontent.com/iarna/App-Every/master/packed/every' | perl -X - -n  -l'`

*  Example:

    `% cron-every 3 hours ls`


        PATH=/home/foilo/cappucino/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/foilo/.rvm/bin
        LOCKFILE=/tmp/every_lock_b8d65f1a8f00500bbda75fc44a4d5f88
        SHELL=/bin/zsh
        54 */3 * * * [ ! -f $LOCKFILE -o ! -d /proc/`[ -f $LOCKFILE ] && cat $LOCKFILE` ] && ( echo $$ > $LOCKFILE ; cd "/home/foilo";  ls  ; rm $LOCKFILE )



Perl MooseX Skeleton
------------------------
My Own ... only for private use ;)
==========


FUSE Tips & Tricks
------------------------
Basic
==========
Example invocation using sshfs:

        `afuse -o mount_template="sshfs %r:/ %m" \
                -o unmount_template="fusermount -u -z %m" \
                   mountpoint/`

Now try `ls mountpoint/user@host/`.



Linux - i386 support for x86_64
------------------------
RPM based
* `# yum -y install glibc-devel.i386 libstdc++-devel.i386`
* `# yum -y install glibc-devel.i686 glibc-devel ibstdc++-devel.i686`
* `# zypper in glibc-devel-32bit`

debian
* `$ sudo apt-get install g++-multilib libc6-dev-i386`


Example

`$ gcc -m32 -o output32 hello.c`


raspi tips & notes
------------------------
Only some hints for raspi-wheezy
==================================

* Nodejs-latest ( >0.10.29 )


            cd /tmp && wget http://node-arm.herokuapp.com/node_latest_armhf.deb
            dpkg -i node_latest_armhf.deb


Simple gist to show the aptly magic :)
------------------------
[Aptly](http://www.aptly.info/#usage) Real-Live example
=============================================================

Example to build a grml-repo with extras.

Install Repo
======================
`$ wget -qO- http://deb.foilo.de/repo-key.asc | sudo apt-key add --`   

`$ echo 'deb http://deb.foilo.de/ ubuntu main ' > /etc/apt/sources.list.d/foilo.lis`

`$ apt-get update`

For Publishing
================

* first install gpg & create new key with `gpg --gen-key` 

* Edit all your needed arch's to `~/.aptly.conf`. Example:
 


            {
              "rootDir": "/var/www/aptly",
              "downloadConcurrency": 4,
              "architectures": ["amd64","armhf"],
              "dependencyFollowSuggests": false,
              "dependencyFollowRecommends": false,
              "dependencyFollowAllVariants": true,
              "dependencyFollowSource": false,
              "gpgDisableSign": false,
              "gpgDisableVerify": false,
              "downloadSourcePackages": false,
              "ppaDistributorID": "ubuntu",
              "ppaCodename": ""
            }
 

* Now make http config or use `aptly serve` to listen on port 8080 & serve your repo's

* Example lighttp config:

            $HTTP["url"] =~ "^/apt($|/)" {
                    server.dir-listing = "enable"
                    server.document-root = "/var/www/aptly/public/"
            }
 

Add local files
============================

Create a a new repo with `aptly repo create <testing>` or use a mirror

            aptly repo add testing pac-4.5.4-all.deb

Add files from other repo
=============================


           aptly -dep-follow-all-variants=true  mirror create grml-testing http://deb.grml.org/ grml-testing 
           aptly mirror update grml-testing


* Now we copy `grml-autoconfig` from `grml-testing` to our repo 

           aptly -dep-follow-all-variants=true repo import grml-testing testing grml-autoconfig

           
            
* Add package from ppa

            aptly -architectures="amd64"  mirror create scribes http://ppa.launchpad.net/mystilleef/scribes-daily/ubuntu quantal main        
            
            
* Create snapshot from mirror

            aptly snapshot create grml-snap from mirror grml-test 
            
            
-------------------------------------------------------------------


Made your own deb-repo
=======================

* Download & read aptly mini-how-to 
  [aptly-main](http://www.aptly.info/)


Start - Dont forgett this!
===============
Your should have gnugpg keys!!! You will need it for sign & publish

* Create grml-test mirror as debian base 
  `aptly -architectures="amd64"  mirror create grml-test http://deb.grml.org/ grml-testing`


Add own ppa to your Repo
==============
Your should beginn with  
* Add a upstream ppa to oure list
  `aptly mirror create jdownloader-latest http://ppa.launchpad.net/jd-team/jdownloader/ubuntu trusty`
  `aptly mirror update jdownloader-latest`
* Now we add `jdownloader-latest` to our repo testing and main
  `aptly repo import jdownloader-latest testing main`
  `aptly publish update testing`


* Create local repo, for your own shit ( local debs )
   `aptly repo create local-repo`
   `aptly repo add testing node_0.10.29-1_amd64.deb`

* Publish
   `aptly publish update ubuntu`

* Lighttpd.conf ( Bsp: /etc/lighttpd/conf-enabled/20-main.conf )


        $HTTP["host"] =~ "^(?i:deb\.foilo\.de(?::\d+)?)$" {
                server.dir-listing = "enable"
             server.document-root = "/var/www/aptly/public/"
        }






pptpd simple setup
------------------------
Basic Networksetup
=======================

* should be in startup script

                iptables -A POSTROUTING -t nat -o ppp+ -j MASQUERADE
                echo 1 > /proc/sys/net/ipv4/ip_forward


PPTPD Setup 
========

* install pptpd `apt-get install pptpd`

* Edit remoteip and ip ranges at `/etc/pptpd.conf`

* edit user accounts at `/etc/ppp/chap-secrets`

                #username      server      password    remote IP addresses
                pptpusername   pptpd secretpassword    45.45.45.45
      
* Restart the PPtP daemon `service pptpd restart`



PPTP Client
===============

                pptpsetup –create –server yourserver.com –username pptpusername –password secretpassword –start


* Script for cronjob for restart as attach





Last Notes:
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


