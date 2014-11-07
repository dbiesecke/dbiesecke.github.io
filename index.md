![My WIki](images/logo.jpg)

- - - - - - 

<script type="text/javascript" src="http://www.commandlinefu.com/commands/by/dbiesecke/json/clfwidget/"></script> <script type="text/javascript">
function clfwidget(commands) {
    var commandsHtml = [];
    for (var i=0; i<Math.min(5, commands.length); ++i) {
        var command = commands[i].command;
        var summary = commands[i].summary;
        var url = commands[i].url;
        commandsHtml.push('<li><a href="'+url+'">'+summary+'</a><br/><code>$ '+command+'</code></li>');
    }
    var listHtml = '<ul>'+commandsHtml.join('')+'</ul>';
    var widgetHtml = listHtml+'<p><a href="http://www.commandlinefu.com">commandlinefu.com</a></p>';
    document.getElementById('commandlinefu_list').innerHTML = widgetHtml;
}
</script>

<div id="commandlinefu_list"></div>

---------------------

# Docker & logstash... and (free) multiple online services!

Register on the following services & make a gist with your OWN settings, have fun to collect!


  * [Papertrail](https://papertrailapp.com/?thank=7cfb38)
  * [Logentries](https://logentries.com/learnmore?code=c4TEpHn52LKeRN9Yb6Aku8XZQxfWUhws)
  * Make a log dir, like /log on your MAIN host like: `mkdir /log && ln -f /var/log/syslog /log/syslog`


      docker run  --name=logstash \
        -e LOGSTASH_CONFIG_URL=https://gist.githubusercontent.com/dbiesecke/2c49b8c80f42186d78e5/raw/logstash-1.conf \
        -p 9292:9292 \
        -p 9200:9200 -p 554:514/udp -p 555:514 \
        -v /log:/log pblittle/docker-logstash
        
   * Lets write som logs! 
   * Write directly over tcp: `echo das | nc -v YOURHOST 555`
   * Lets scrap logs with logstash:`ln -f /var/log.... /log/syslog` 
   * Write debug stuff: `echo blablalba > /log/das`
          ......