Pseudo TV Live
========================================


* Mit diesen Plugin könnt ihr Video Addons,Playlisten, Serien, etc als EPG anordnen und erzeugt somit ein echtes "TV-Feeling".



# Neuen Channel hinzufügen.
---------------------------------
* Neue Channels sollten nur über das "pseudo Companion" Plugin hinzugefügt werden.  

![pseudotv-edit-1.gif](http://home.forward.pw/my/kodi/pseudo-add-neu-plugin.gif)



## Variante 1
----------------
* Alternative über das Config menü

![pseudotv-edit-1.gif](http://home.forward.pw/my/kodi/pseudotv-edit-1.gif)


## Pseudo Companion Config
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







