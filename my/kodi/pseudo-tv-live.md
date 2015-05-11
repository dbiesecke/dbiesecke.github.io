Pseudo TV Live
========================================

[![](http://i.imgur.com/NvgA34Y.png)](http://forum.kodi.tv/showthread.php?tid=169032)

* Dieses Plugin ermöglicht per XML File die möglichkeit automatisch Plugin's in datein zu verwandeln.

| Name                       	| DL 	| INFO 	| BETA?	|
|----------------------------	|----	|------	|-----	|
| Pseudo TV Live        	|[repo](https://github.com/Lunatixz/XBMC_Addons/blob/master/zips/repository.lunatixz/repository.lunatixz-1.0.zip)    	|      	[forum.kodi.tv](http://forum.kodi.tv/showthread.php?tid=169032)												|  YES!	|



Config
----------------------------------

Nachfolgend kommen Beispiel config's für die settings2.mxl

    Genre|Type|Source/Path|Exclusion,Exclusion|limit|1|Folder Name
    
    #Holt 2000 Amazon filme aus der Kategorie "Beliebt"
    Movies|Plugin|plugin.video.prime_instant/Filme/Beliebt/|""|2000|1|""

    #Holt sich Datein aus einer Youtube Playlist & ordnet sie der Serie "Elfen Lied" zu
    Episodes|Youtube|PLWtmJEyHDI8OGBZb0m0zX-zH6q3jmll5G|""|100|2|Elfen Lied
    Episodes|Youtube|PLWtmJEyHDI8Notsg3_gTp0PR33qEbnLPC|""|100|2|Highschool Of The Dead   
    
    #Kommt auf das Plugin an, ob die TV serie richtig gescrapt werden kann
    TVShows|Plugin|plugin.video.animeanime/Serien/K/Kantai.Collection.KanColle/Season.1/|""|25|1|""  
    
    Episodes|Plugin|plugin.video.animetube/Neu|""|200|1|""
    Movies|Plugin|plugin.video.animetube/Filme|""|100|1|""







