XBMC.MyLibrary
=======

Allgemeine Tips
----------------

  * MyLib versucht die Titel anhand des Titelnames 
  * Wenn die Serie absol



MyVideo Neuste & Top Filme
-------------------------------

	
	<!--    ** Durchsucht das MyVideo Plugin unter Film/Top Filme nach neuen filmen-->
	
	<MyVideoFilme path="plugin://plugin.video.myvideo_de" recursive="true"  prefix="(MyVideo) " >			
		<subfolder name="Filme/Top Filme" 
			  type="movies" movie_set=" MyVideo (Neue)" />	
		<subfolder name="Filme/Neuste Filme" 
			  type="movies" movie_set=" MyVideo (Neue)" />				
	</MyVideoFilme>


Get Your Youtube Music Video's
-------------------------------


	<!-- Holt sich alle Music Videos aus deinen Youtube Plugin/Account -->
	
	<YOU path="plugin://plugin.video.youtube" recursive="true" >
		<subfolder name="Meine Favoriten" type="music_videos"         />
		<subfolder name="Meine Abonnements" type="music_videos"       />
		<subfolder name="Meine Wiedergabelisten" type="music_videos"  />
			
	</YOU>
	

Amazon Prime Plugin, parse Serien	
------------------------------------

	  <Amazon path="plugin://plugin.video.prime_instant" recursive="true" regex_name="false" >
	      <subfolder name="Filme/Beliebt"  max_videos="100" recursive="true" type="movies" />
	      <subfolder name="Serien/Meine Watchlist/Drawn Together"  force_series="Drawn Together" recursive="true" type="episodes" />	
	      <subfolder name="Serien/Meine Watchlist/Ugly Americans"  force_series="Ugly Americans" recursive="true" type="episodes" />	
	      <subfolder name="Serien/Meine Watchlist/Anger Management"  force_series="Anger Management" recursive="true" type="episodes" />      
	      <subfolder name="Serien/Meine Watchlist/Under the Dome"  force_series="Under the Dome" recursive="true" type="episodes" />           
	      <subfolder name="Serien/Meine Watchlist/Defiance"  force_series="Defiance" recursive="true" type="episodes" />           
	      <subfolder name="Serien/Meine Watchlist/Akte X"  force_series="The X-Files" recursive="true" type="episodes" />	      
	      <subfolder name="Serien/Meine Watchlist/Ally McBeal"  force_series="Ally McBeal" recursive="true" type="episodes" />	      
	      <subfolder name="Serien/Meine Watchlist/Fringe: Grenzfälle des FBI"  force_series="Fringe" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/Two and a Half Men"  force_series="Two and a Half Men" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/The Big Bang Theory"  force_series="The Big Bang Theory" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/Navy CIS"  force_series="NCIS" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/Dexter"  force_series="Dexter" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/Breaking Bad"  force_series="Breaking Bad" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/2 Broke Girls"  force_series="2 Broke Girls" recursive="true" type="episodes" />
	      <subfolder name="Serien/Beliebt/The Walking Dead"  force_series="The Walking Dead" recursive="true" type="episodes" />
	      <subfolder name="Serien/Meine Watchlist/Rogue Hero"  force_series="Rogue Hero" recursive="true" type="episodes" />
	      <subfolder name="Serien/Meine Watchlist/Samurai Girls"  force_series="Samurai Girls" recursive="true" type="episodes" />
	      <subfolder name="Serien/Meine Watchlist/Der Tatortreiniger"  force_series="Der Tatortreiniger" recursive="true" type="episodes" />	      
	      <subfolder name="Serien/Meine Watchlist/Californication"  force_series="Californication" recursive="true" type="episodes" />	
	      <subfolder name="Serien/Meine Watchlist/Little Britain - Specials"  force_series="Little Britain - Specials" recursive="true" type="episodes" />	 	      
	      <subfolder name="Serien/Meine Watchlist/Weeds"  force_series="Weeds" recursive="true" type="episodes" />	
	      <subfolder name="Serien/Meine Watchlist/Stromberg"  force_series="Stromberg" recursive="true" type="episodes" />	
	      <subfolder name="Serien/Meine Watchlist/How I Met Your Mother"  force_series="How I Met Your Mother" recursive="true" type="episodes" />	
	      <parser>
		      <regexp>([\w\s'-_]+)\.E[\d+]\.([\w\s*'-]*)</regexp>
	      </parser> 	
	  </Amazon>
	  

	
All Complete Animes from Anime Plugin
----------------------------------------


	<CompletAnimes path="plugin://plugin.video.animeanime" recursive="true" regex_name="false" >

	  <subfolder name="Genres/Action/kidou senshi zeta gundam" force_series="Mobile Suit Zeta Gundam" recursive="true" type="episodes" />
	  <subfolder name="Genres/Action/kidou Senshi Gundam ZZ" force_series="Mobile Suit Gundam ZZ" recursive="true" type="episodes" />
	  <subfolder name="Genres/Action/kidou Shin Seiki Gundam X" force_series="After War Gundam X" recursive="true" type="episodes" />
	    <subfolder name="Serien/H/Hakuouki Shinsengumi Kitan" force_series="Hakuouki Shinsengumi Kitan" recursive="true" type="episodes" />
	    <subfolder name="Serien/O/Ookami Shoujo to Kuro Ouji" force_series="Ookami Shoujo to Kuro Ouji" recursive="true" type="episodes" />
	    <subfolder name="Serien/H/Higurashi" force_series="Higurashi" recursive="true" type="episodes" />
	    <subfolder name="Serien/G/Grisaia no Kajitsu" force_series="Grisaia no Kajitsu" recursive="true" type="episodes" />
	    <subfolder name="Serien/A/Akatsuki no Yona" force_series="Akatsuki no Yona" recursive="true" type="episodes" />
	    <subfolder name="Serien/H/Haikyuu!!" force_series="Haikyuu!!" recursive="true" type="episodes" />
	    <subfolder name="Serien/T/Tokyo ESP" force_series="Tokyo ESP" recursive="true" type="episodes" />
	    <subfolder name="Serien/L/Log Horizon" force_series="Log Horizon" recursive="true" type="episodes" />
	    <subfolder name="Serien/R/Rail Wars!" force_series="Rail Wars!" recursive="true" type="episodes" />
      </CompletAnimes>
	
			
Selected Anime List & use Parser
------------------------


    <Serien path="plugin://plugin.video.animeanime" recursive="true" regex_name="false" >
	  <subfolder name="Serien/H/Hunter X Hunter" force_series="Hunter X Hunter" recursive="true" type="episodes" />
	  <subfolder name="Serien/B/Bleach" force_series="Bleach" recursive="true" type="episodes" />	
	  <subfolder name="Airing Anime/One Piece" force_series="One Piece" recursive="true" type="episodes" />
	  <subfolder name="Serien/F/Fairy Tail" force_series="Fairy Tail" recursive="true" type="episodes" />
	  <subfolder name="Serien/M/Mirai Nikki" force_series="Mirai Nikki" recursive="true" type="episodes" />	
	  <subfolder name="Serien/S/Sword Art Online" force_series="Sword Art Online" recursive="true" type="episodes" />	
	  <subfolder name="Serien/G/Guilty Crown" force_series="Guilty Crown" recursive="true" type="episodes" />	
	  <subfolder name="Serien/D/Deadman Wonderland" force_series="Deadman Wonderland" recursive="true" type="episodes" />	
	  <subfolder name="Serien/A/Afro Samurai" force_series="Afro Samurai" recursive="true" type="episodes" />	
	  <subfolder name="Serien/A/Air" force_series="Air" recursive="true" type="episodes" />					  
	  <subfolder name="Serien/T/Trinity Seven" force_series="Trinity Seven" recursive="true" type="episodes" />
	  <subfolder name="Serien/M/Monster" force_series="Monster" recursive="true" type="episodes" />
	  <subfolder name="Serien/S/Spice and Wolf" force_series="Spice and Wolf" recursive="true" type="episodes" />
	  <subfolder name="Serien/A/Arcana Famiglia" force_series="Arcana Famiglia" recursive="true" type="episodes" />
	  <subfolder name="Serien/P/Psycho Pass" force_series="Psycho Pass" recursive="true" type="episodes" />
	  <subfolder name="Serien/L/Love Stage!!" force_series="Love Stage!!" recursive="true" type="episodes" />	
	  <subfolder name="Serien/A/Aldnoah.Zero" force_series="Aldnoah.Zero" recursive="true" type="episodes" />	
	  <parser>
		  <regexp>([\w\s'-_]+)\.E[\d+]\.([\w\s*'-]*)</regexp>
	  </parser> 				
    </Serien>
		 