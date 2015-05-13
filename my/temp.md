App-CloudMining: perl app to show stats from cloud mining provider like zencloud
builder-litecoin: Docker builder for building the litecoin daemon
dashing-cloudmining-dash: the dashboard for my cloud stats
dbiesecke.github.io: no description
docker-bitcoind: Docker image that runs a bitcoind node in a container for easy deployment
docker-graphite-statsd: Docker image for Graphite & Statsd
docker-mogilefs: Docker image of mogilefs
dotfiles: no description
MangaDownloader: Little tool to download mangas from various sites.
manga_downloader: Cross-platform, multi-site, multi-threaded manga downloader with over 5000 distinct mangas.  Includes support for automated downloading via external .xml file and conversion for viewing on the Kindle.
Net-LFTP: Perl extension to LFTP
plugin.video.animeanime: fork of plugin.video.animeanime
plugin.video.burningseries: little fork to support "one-click-play"
plugin.video.xstream: plugin.video.xstream
unix-nginx-bundle: make your own nginx
x13-cpuminer: no description
---------------------------- GIST's ----------------

[Notes]()

   * [manga tools](https://gist.github.com/d8af4f395c58575ac0ae)
   * [test logstash & docker, whats a Magic!](https://gist.github.com/2c49b8c80f42186d78e5)
   * [CGMiner API Example](https://gist.github.com/9c5032c467604d705c42)
   * [Graphite  Docker & collected](https://gist.github.com/53c51e71efcb32ee6e8c)
   * [Startup / Persistence](https://gist.github.com/ba359f53f392d513cdea)
   * [Perl MooseX Skeleton](https://gist.github.com/90ae2f1e5a28463f2527)
   * [FUSE Tips & Tricks](https://gist.github.com/b00eff217ad00069933d)
   * [Linux - i386 support for x86_64](https://gist.github.com/414aa7313588c583d63f)
   * [raspi tips & notes](https://gist.github.com/2b8c8819c737a6f965e0)
   * [Simple gist to show the aptly magic :)](https://gist.github.com/5ecd3d5d2de50bcd30aa)
   * [pptpd simple setup](https://gist.github.com/eb10bbc7bc63d289d347)


manga tools
------------------------
Hint:
Best Tools
##############

* [manga_downloader](https://github.com/jiaweihli/manga_downloader)
* [KindleComicConverter](https://github.com/ciromattia/kcc)
* 



## Usage

`manga.py [options] <manga name> <manga name> <etc.>`

The script will offer a choice of 3 manga sites, it will default to the first upon pressing 'enter'.

After selecting a site, the script will output a list of all chapters of the series it has found on
the site you selected.

When it prompts "Download which chapters?", type in the ones you want delimited by '-' and ','.
You can also type 'all' if you did not specify `--all` before.

### Options

> `--version`

show program's version number and exit

> `-h, --help`

show this help message and exit

> `--all`

Download all available chapters.

> `-d <download path>, --directory<download path>`

The destination download directory. Defaults to a directory named after the manga.

> `--overwrite`

Overwrites previous copies of downloaded chapters.

> `-t <number>, --threads<number>`

Limits the number of chapter threads to the user specified value. Default value is `3`.

> `--verbose`

Verbose output.

> `-x <xmlfile path>, --xml<xmlfile path>`

Parses the `.xml` file and downloads all chapters newer than the last chapter downloaded for the
listed mangas.

> `-z, --zip`

Downloads using `.zip` compression.  Omitting this option defaults to `.cbz.`

> `-c, --convertFiles`

Converts the files that are downloaded to a Format/Size ratio acceptable to the device specified by
the `device` parameter. The converted images are saved in the directory specified by the
`outputDirectory` paraemter.

> `--device`

Specifies the target device for the image conversion.

> `--convertDirectory`

Converts the image files stored in the directory specified by the `inputDirectory` parameter. Stores
the images in the directory specified by the `outputDirectory` Parameter

> `--inputDirectory`

The directory containing the images to convert when `convertDirectory` is specified.

> `--outputDirectory`

The directory to store the converted Images. Omitting this option defaults to
`DOWNLOAD_PATH/Pictures`.

### Usage

> `manga.py -d "C:\Documents and Settings\admin\Documents\Manga\" -z Bleach`

On a Windows machine, downloads 'Bleach' to `C:\Documents and Settings\admin\Documents\Manga\`,
using `.zip` compression.

> `./manga.py --overwrite Bleach`

On a Linux/Unix machine, downloads 'Bleach' to `./Bleach`, using `.cbz` compression and overwriting
previously downloaded chapters.

> `1,2,9-12`

Downloads chapters `1`, `2`, and `9` through `12`

> `all`

Downloads all chapters

> `./manga.py -x example.xml`

Parses `example.xml` to run the script.





test logstash & docker, whats a Magic!
------------------------
Hint:
# Docker & logstash... and (free) multiple online services!

Register on the following services & make a gist with your OWN settings, have fun to collect!


  * [Papertrail](https://papertrailapp.com/?thank7cfb38)
  * [Logentries](https://logentries.com/learnmore?codec4TEpHn52LKeRN9Yb6Aku8XZQxfWUhws)
  * Make a log dir, like /log on your MAIN host like: `mkdir /log && ln -f /var/log/syslog /log/syslog`


    docker run --namelogstash \
        -e LOGSTASH_CONFIG_URLhttps://gist.githubusercontent.com/dbiesecke/2c49b8c80f42186d78e5/raw/logstash-1.conf \
        -v /var/log/syslog:/log/syslog -v /log:/log \
        -p 555:555 -p 514:514/udp -p 9292:9292 \
        -e VIRTUAL_HOST"logs.nated.at" -e VIRTUAL_PORT"9292" \
        pblittle/docker-logstash
        
   * Lets write som logs! 
   * Write directly over tcp: `echo das | nc -v YOURHOST 555`
   * Lets scrap logs with logstash:`ln -f /var/log.... /log/syslog` 
   * Write debug stuff: `echo blablalba > /log/das`
          ......





CGMiner API Example
------------------------
Hint:
Example ( Antminer-3 )


`echo '{"command":"summary","parameter":"0"}' | nc -v antminer-1 4028` 


          {
            "STATUS": [
              {
                "STATUS": "S",
                "When": 1415057522,
                "Code": 11,
                "Msg": "Summary",
                "Description": "cgminer 3.12.0"
              }
            ],
            "SUMMARY": [
              {
                "Elapsed": 112838,
                "GHS 5s": 416.81,
                "GHS av": 419.96,
                "Found Blocks": 0,
                "Getworks": 11712,
                "Accepted": 6684,
                "Rejected": 40,
                "Hardware Errors": 215,
                "Utility": 3.55,
                "Discarded": 839931,
                "Stale": 6,
                "Get Failures": 8,
                "Local Work": 25336132,
                "Remote Failures": 0,
                "Network Blocks": 234,
                "Total MH": 47387095720.383,
                "Work Utility": 5866.74,
                "Difficulty Accepted": 11225402.12488,
                "Difficulty Rejected": 67713.737557,
                "Difficulty Stale": 12288,
                "Best Share": 7466,
                "Device Hardware%": 0.0019,
                "Device Rejected%": 0.6137,
                "Pool Rejected%": 0.599,
                "Pool Stale%": 0.1087,
                "Last getwork": 1415057522
              }
            ],
            "id": 1
          }


Example for dashing

$VAR1  {
          'summary' > [
                         {
                           'accepted' > 6769,
                           'local_work' > 25749250,
                           'last_getwork' > 1415059306,
                           'ghs_av' > '420.01',
                           'pool_rejected_percentage' > '0.5899',
                           'device_rejected_percentage' > '0.6041',
                           'remote_failures' > 0,
                           'difficulty_rejected' > '67713.737557',
                           'found_blocks' > 0,
                           'rejected' > 40,
                           'work_utility' > '5867.53',
                           'ghs_5s' > '430.31',
                           'elapsed' > 114620,
                           'hardware_errors' > 216,
                           'pool_stale_percentage' > '0.107',
                           'discarded' > 856511,
                           'device_hardware_percentage' > '0.0019',
                           'difficulty_accepted' > '11399482.12488',
                           'network_blocks' > 239,
                           'get_failures' > 8,
                           'difficulty_stale' > '12288',
                           'getworks' > 11928,
                           'utility' > '3.54',
                           'best_share' > 7466,
                           'stale' > 6,
                           'total_mh' > '48142047891.6372'
                         }
                       ],
          'status' > [
                        {
                          'msg' > 'summary',
                          'code' > 11,
                          'when' > 1415059306,
                          'description' > 'cgminer_3.12.0',
                          'status' > 's'
                        }
                      ],
          'id' > 1
        };
$VAR1  {
          'status' > [
                        {
                          'description' > 'cgminer_3.12.0',
                          'when' > 1415059306,
                          'status' > 's',
                          'msg' > '3_pool(s)',
                          'code' > 7
                        }
                      ],
          'id' > 1,
          'pools' > [
                       {
                         'user' > '1jhtq38ezyskhzgvrr7a6ebrzutprctwcn',
                         'stratum_active' > 'true',
                         'status' > 'alive',
                         'discarded' > 508595,
                         'pool_stale_percentage' > '0.2022',
                         'proxy_type' > '',
                         'rejected' > 36,
                         'priority' > 0,
                         'difficulty_accepted' > '5999888.423512',
                         'diff1_shares' > 70099,
                         'stale' > 6,
                         'pool' > 0,
                         'best_share' > 3477,
                         'getworks' > 7202,
                         'difficulty_stale' > '12288',
                         'get_failures' > 8,
                         'stratum_url' > 'stratum.nicehash.com',
                         'has_gbt' > 'false',
                         'accepted' > 3380,
                         'long_poll' > 'n',
                         'pool_rejected_percentage' > '1.0616',
                         'has_stratum' > 'true',
                         'diff' > '2.05k',
                         'quota' > 1,
                         'last_share_time' > '0:00:35',
                         'last_share_difficulty' > '2048',
                         'url' > 'stratum+tcp://stratum.nicehash.com:3334',
                         'difficulty_rejected' > '64512',
                         'proxy' > '',
                         'remote_failures' > 0
                       },
                       {
                         'stratum_active' > 'false',
                         'user' > '1jhtq38ezyskhzgvrr7a6ebrzutprctwcn',
                         'proxy_type' > '',
                         'priority' > 1,
                         'rejected' > 4,
                         'status' > 'alive',
                         'discarded' > 347916,
                         'pool_stale_percentage' > '0',
                         'diff1_shares' > 67770,
                         'difficulty_accepted' > '5399593.701368',
                         'get_failures' > 0,
                         'difficulty_stale' > '0',
                         'getworks' > 4718,
                         'stale' > 0,
                         'pool' > 1,
                         'best_share' > 7466,
                         'accepted' > 3389,
                         'has_gbt' > 'false',
                         'stratum_url' > '',
                         'long_poll' > 'n',
                         'pool_rejected_percentage' > '0.0593',
                         'has_stratum' > 'true',
                         'last_share_time' > '16:03:25',
                         'quota' > 1,
                         'diff' > '1.02k',
                         'difficulty_rejected' > '3201.737557',
                         'proxy' > '',
                         'url' > 'stratum+tcp://stratum.westhash.com:3334',
                         'remote_failures' > 0,
                         'last_share_difficulty' > '1024'
                       },
                       {
                         'user' > '1jhtq38ezyskhzgvrr7a6ebrzutprctwcn',
                         'stratum_active' > 'false',
                         'status' > 'alive',
                         'pool_stale_percentage' > '0',
                         'discarded' > 0,
                         'proxy_type' > '',
                         'rejected' > 0,
                         'priority' > 2,
                         'difficulty_accepted' > '0',
                         'diff1_shares' > 0,
                         'stale' > 0,
                         'pool' > 2,
                         'best_share' > 0,
                         'get_failures' > 0,
                         'difficulty_stale' > '0',
                         'getworks' > 8,
                         'stratum_url' > '',
                         'has_gbt' > 'false',
                         'accepted' > 0,
                         'pool_rejected_percentage' > '0',
                         'has_stratum' > 'true',
                         'long_poll' > 'n',
                         'diff' > '2',
                         'quota' > 1,
                         'last_share_time' > '0',
                         'last_share_difficulty' > '0',
                         'difficulty_rejected' > '0',
                         'proxy' > '',
                         'url' > 'stratum+tcp://de3.miningpool.co:3921',
                         'remote_failures' > 0
                       }
                     ]
        };
$VAR1  {
          'devs' > [
                      {
                        'name' > 'bmm',
                        'asc' > 0,
                        'last_share_time' > 1415059271,
                        'last_share_pool' > 0,
                        'last_share_difficulty' > '2048',
                        'no_device' > 'false',
                        'difficulty_rejected' > '62593.737557',
                        'enabled' > 'y',
                        'last_valid_work' > 1415059306,
                        'accepted' > 6722,
                        'device_rejected_percentage' > '0.5584',
                        'mhs_5s' > '405562.37',
                        'difficulty_accepted' > '11315514.12488',
                        'total_mh' > '48142047891.6372',
                        'diff1_work' > 11209005,
                        'id' > 0,
                        'mhs_av' > '420012.8',
                        'utility' > '3.52',
                        'device_elapsed' > 114620,
                        'temperature' > '40.5',
                        'device_hardware_percentage' > '0.0019',
                        'status' > 'alive',
                        'hardware_errors' > 216,
                        'rejected' > 37
                      }
                    ],
          'id' > 1,
          'status' > [
                        {
                          'when' > 1415059306,
                          'description' > 'cgminer_3.12.0',
                          'status' > 's',
                          'msg' > '1_asc(s)',
                          'code' > 9
                        }
                      ]
        };







Graphite  Docker & collected
------------------------
Hint:
Graphite easy install:

Source: [docker-graphite-statsd](https://github.com/dbiesecke/docker-graphite-statsd)

        docker run -d \
        --name graphite \
        -e VIRTUAL_HOST"graph.foilo.de" \
        -p 2003:2003 \
        -p 8125:8125/udp \
        dbiesecke/docker-graphite-statsd
  
  
Fill your graphs!


* ` echo "sample.gauge:9|g" | nc -u -w0 grap.foilo.de 8125`

* Sample event over HTTP: 

      `curl -X POST "http://graphite/events/" 
      -d '{"what": "Event - deploy", "tags": "deploy", 
      "data": "deploy of master branch happened at Fri Jan  3 22:34:41 UTC 2014"}'`


Ext


* [statistik](https://github.com/godmodelabs/statistik) is a nice node lib & cli for first steps.


                $ docker build -tdbiesecke/statistik https://gist.githubusercontent.com/dbiesecke/53c51e71efcb32ee6e8c/raw/Dockerfile.statistik
                


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

* [Blog-digitalocean](https://www.digitalocean.com/community/tutorials/how-to-configure-statsd-to-collect-arbitrary-stats-for-graphite-on-ubuntu-14-04)

Dashing

* [Plugin](https://gist.github.com/Ulrhol/5088efcc94de2fecad5e)
* [Plugin-Simple](https://gist.github.com/joerayme/5934555)






Startup / Persistence
------------------------
Hint:
App::Every

Makes a cron entry with 2x simple parameters.

* Alias: `alias cron-every'curl -sk 'https://raw.githubusercontent.com/iarna/App-Every/master/packed/every' | perl -X - -n  -l'`

*  Example:

    `% cron-every 3 hours ls`


        PATH/home/foilo/cappucino/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/foilo/.rvm/bin
        LOCKFILE/tmp/every_lock_b8d65f1a8f00500bbda75fc44a4d5f88
        SHELL/bin/zsh
        54 */3 * * * [ ! -f $LOCKFILE -o ! -d /proc/`[ -f $LOCKFILE ] && cat $LOCKFILE` ] && ( echo $$ > $LOCKFILE ; cd "/home/foilo";  ls  ; rm $LOCKFILE )






Perl MooseX Skeleton
------------------------
Hint:
My Own ... only for private use ;)






FUSE Tips & Tricks
------------------------
Hint:
Basic

Example invocation using sshfs:

  	`afuse -o mount_template"sshfs %r:/ %m" \
	        -o unmount_template"fusermount -u -z %m" \
	           mountpoint/`

Now try `ls mountpoint/user@host/`.






Linux - i386 support for x86_64
------------------------
Hint:
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
Hint:
Only some hints for raspi-wheezy


* Nodejs-latest ( >0.10.29 )


            cd /tmp && wget http://node-arm.herokuapp.com/node_latest_armhf.deb
            dpkg -i node_latest_armhf.deb





Simple gist to show the aptly magic :)
------------------------
Hint:
[Aptly](http://www.aptly.info/#usage) Real-Live example


Example to build a grml-repo with extras.

Install Repo

`$ wget -qO- http://deb.foilo.de/repo-key.asc | sudo apt-key add --`   

`$ echo 'deb http://deb.foilo.de/ ubuntu main ' > /etc/apt/sources.list.d/foilo.lis`

`$ apt-get update`

For Publishing


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

            $HTTP["url"] ~ "^/apt($|/)" {
                    server.dir-listing  "enable"
                    server.document-root  "/var/www/aptly/public/"
            }
 

Add local files


Create a a new repo with `aptly repo create <testing>` or use a mirror

            aptly repo add testing pac-4.5.4-all.deb

Add files from other repo



           aptly -dep-follow-all-variantstrue  mirror create grml-testing http://deb.grml.org/ grml-testing 
           aptly mirror update grml-testing


* Now we copy `grml-autoconfig` from `grml-testing` to our repo 

           aptly -dep-follow-all-variantstrue repo import grml-testing testing grml-autoconfig

           
            
* Add package from ppa

            aptly -architectures"amd64"  mirror create scribes http://ppa.launchpad.net/mystilleef/scribes-daily/ubuntu quantal main        
            
            
* Create snapshot from mirror

            aptly snapshot create grml-snap from mirror grml-test 
            
            
-------------------------------------------------------------------


Made your own deb-repo


* Download & read aptly mini-how-to 
  [aptly-main](http://www.aptly.info/)


Start - Dont forgett this!

Your should have gnugpg keys!!! You will need it for sign & publish

* Create grml-test mirror as debian base 
  `aptly -architectures"amd64"  mirror create grml-test http://deb.grml.org/ grml-testing`


Add own ppa to your Repo

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


        $HTTP["host"] ~ "^(?i:deb\.foilo\.de(?::\d+)?)$" {
                server.dir-listing  "enable"
             server.document-root  "/var/www/aptly/public/"
        }









pptpd simple setup
------------------------
Hint:
Basic Networksetup


* should be in startup script

	 	iptables -A POSTROUTING -t nat -o ppp+ -j MASQUERADE
      		echo 1 > /proc/sys/net/ipv4/ip_forward


PPTPD Setup 


* install pptpd `apt-get install pptpd`

* Edit remoteip and ip ranges at `/etc/pptpd.conf`

* edit user accounts at `/etc/ppp/chap-secrets`

		#username      server      password    remote IP addresses
      		pptpusername   pptpd secretpassword    45.45.45.45
      
* Restart the PPtP daemon `service pptpd restart`



PPTP Client


		pptpsetup –create –server yourserver.com –username pptpusername –password secretpassword –start


* Script for cronjob for restart as attach








