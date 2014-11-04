![My WIki](images/logo.jpg)

<script src="https://d26b395fwzu5fz.cloudfront.net/latest/keen.min.js"></script>


  <script type="text/javascript">

var client = new Keen({
  projectId: "544db74433e4061c57579de5",
  readKey: "b1e2a66c5398880e752bd40808f2c8b2463a62883413b48bf640644d2e79143dc34fea6a6841e534d0e16a091c029e177cd5cac0c00690c6d9345ce2d6220a9387b664d6346d66ef0513e09579c307effc5a7b95632d9992506c0a6b8ecdd89acf60e412b8aab8a3e987aae3d2e5c41b"
});
Keen.ready(function(){
  var query = new Keen.Query("average", {
    eventCollection: "Zencloud",
    timeframe: "this_week",
    targetProperty: "current",
    interval: "daily",
    groupBy: "btc_addr"
  });
  client.draw(query, document.getElementById("mychart"), {
    // Custom configuration here
      colors: [ "#ff0000", "#222", "lightblue" ], //
      title: "",        // string or null
      width: 240,       // integer or "auto"
        chartOptions: {
            isStacked: true,
      }
  });
});
  
</script>
<ul>
    <li data-row="1" data-col="1" data-sizex="1" data-sizey="1">
      <div id="mychart"></div>

    </li>
</ul>

- - - - - - 

### Temp

<!-- ZEEF widget start --><iframe src="//zeef.io/block/34887?userId=4884&max_links=10&font_size=13&show_curator=0&color_header_background=050305&color_body_background=666666&color_body_text=ffffff" width="230" height="200" frameborder="0" scrolling="no"></iframe><!-- ZEEF widget end -->


- - - - - -
Based on [Pwn Wiki](http://pwnwiki.io/) 
Curators:

  * [@mubix](https://twitter.com/mubix) [gimmick:TwitterFollow](@mubix)
  * [@WebBreacher](https://twitter.com/webbreacher) [gimmick:TwitterFollow](@WebBreacher)
  * [@tekwizz123](https://twitter.com/tekwizz123) [gimmick:TwitterFollow](@tekwizz123)
  * [@jakx_](https://twitter.com/jakx_) [gimmick:TwitterFollow](@jakx_)
  * [@TheColonial](https://twitter.com/TheColonial) [gimmick:TwitterFollow](@TheColonial)
  * [@Wireghoul](https://twitter.com/Wireghoul)  [gimmick:TwitterFollow](@Wireghoul)
