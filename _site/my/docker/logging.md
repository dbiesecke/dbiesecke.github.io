# Docker & logstash... and (free) multiple online services!
==================================================================


Register on the following services & make a gist with your OWN settings, have fun to collect!


  * [Papertrail](https://papertrailapp.com/?thank=7cfb38)
  * [Logentries](https://logentries.com/learnmore?code=c4TEpHn52LKeRN9Yb6Aku8XZQxfWUhws)
  * Make a log dir, like /log on your MAIN host like: `mkdir /log && ln -f /var/log/syslog /log/syslog`


    docker run --name=logstash \
        -e LOGSTASH_CONFIG_URL=https://gist.githubusercontent.com/dbiesecke/2c49b8c80f42186d78e5/raw/logstash-1.conf \
        -v /var/log/syslog:/log/syslog -v /log:/log \
        -p 555:555 -p 514:514/udp -p 9292:9292 \
        -e VIRTUAL_HOST="logs.nated.at" -e VIRTUAL_PORT="9292" \
        pblittle/docker-logstash
        
   * Lets write som logs! 
   * Write directly over tcp: `echo das | nc -v YOURHOST 555`
   * Lets scrap logs with logstash:`ln -f /var/log.... /log/syslog` 
   * Write debug stuff: `echo blablalba > /log/das`
          ......
          

          
fig.yml
===================


      es:
	image: dockerfile/elasticsearch
	ports:
	  - "9300:9300"
	  - "9200:9200"
	environment:
	  - VIRTUAL_HOST="es.nated.at"
	  - VIRTUAL_PORT="9200"
      logstash:
	image: pblittle/docker-logstash
	ports:
	  - "9292:9292"
	  - "555:555"
	environment:
	  - VIRTUAL_HOST="logstash.nated.at"
	  - VIRTUAL_PORT="9292"
	  - LOGSTASH_CONFIG_URL="https://gist.githubusercontent.com/dbiesecke/2c49b8c80f42186d78e5/raw/logstash-1.conf"
      links:
	  - es

	  
logstash-1.conf
===================


      input {

	stdin {
	  type => "event"
	  format => "json"
	}

      #  file {
      #    type => "syslog"
      #    path => [ "/log/*", "/log2" ]
      #    start_position => "beginning"
      #  }  
	
	tcp {
	  port => 555
	  codec => json
	  type => "trigger"
	  #type => "stdin-type"
	}

	udp {
	  port => 514
	  type => syslog
	}  
	
      }

      filter {
	if [src_ip]  {
	  geoip {
	    source => "host"
	    target => "geoip"
	    add_field => [ "[geoip][coordinates]", "%{[geoip][longitude]}" ]
	    add_field => [ "[geoip][coordinates]", "%{[geoip][latitude]}"  ]
	  }
	  mutate {
	    convert => [ "[geoip][coordinates]", "float" ]
	  }
	}
      }

      output {
      #data.logentries.com:12374
	  elasticsearch {
	    bind_host => "ES_HOST"
	    port => "ES_PORT"
	  }

      }






