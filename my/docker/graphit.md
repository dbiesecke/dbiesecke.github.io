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
* `docker build -t=dbiesecke/statistik https://gist.githubusercontent.com/dbiesecke/53c51e71efcb32ee6e8c/raw/Dockerfile.statistik`


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
 
