# Usefull Notes
- - - - - - 

<div id="commandlinefu_list"></div>


#XBMC with ffmpeg "hack" for debian-wheezy
- - - - - - 
* Aufgrundlich rechtlicher folgen ist die ffmpeg version in keinem offiziellem Repo, damit sind auch "verschlüsselte" streams wie N24 kein problem mehr ;)


        # for Wheezy, it also needs packages from wheezy-backports
        deb https://people.debian.org/~rbalint/ppa/xbmc-ffmpeg xbmc-ffmpeg-wheezy-backports/
        deb http://http.debian.net/debian wheezy-backports main contrib non-free
        Since my signing key is already on the Debian keyring you can use it for authenticating the packages if the debian-keyring package is installed:
        
        gpg --keyring /usr/share/keyrings/debian-keyring.gpg -a --export 21E764DF | sudo apt-key add -


# None
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