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
