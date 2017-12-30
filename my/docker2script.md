# docker2script

[![asciicast](https://asciinema.org/a/7yVERoPBwdy4OT4wkyPe8ogOi.png)](https://asciinema.org/a/7yVERoPBwdy4OT4wkyPe8ogOi)


* Die Grund idee ist das komplette Docker Image zu exportieren (quasi das gesamte system mit finalen binary) & alles mit [makeself](http://makeself.io/) & [proot](http://proot-me.github.io/) in ein ausführbares script zu verwandeln.

## Required
* Makeself (Im Linux packetmanagment - like apt-get install makeself)
* [proot-static](https://github.com/proot-me/proot-static-build/tree/master/static) - die passende datei für hostsystem 
* Docker - Linux Packetmanagment
* Passende Docker Image zum Exportieren ( am besten alpine)

## Notes

* Wenn Dateigröße eine Rolle spielt, dann achtet darauf das ich Alpine OS als Grundlage nehmt, dann wird euer fertiges script oft auch nur eine 1-4mb betragen.
 
##Step By Step

-  Docker Images builden oder per pull vom Dockerhub ziehen: `docker pull bitnn/alpine-xmrig`
-  Die Images muss einmal gestartet werden & für das exportieren brauch wir die docker ID. Dazu starten wir dei Image mit -d  
         

        $ docker run -dit bitnn/alpine-xmrig [scheiß egal was hier steht]
        e23474600c90b22c3f054d60941e304eab70f31ef9806a7d02695970f10a8525

- Wir können nun alle datein die benötigt werden exporieren:
  `$ docker export e23474600c90b22c3 -o xmrig.tar`

- Erstellt euch neuen ordner, entpackt unsere neu erstelltes tar archiv & packt die [proot-static](https://github.com/proot-me/proot-static-build/tree/master/static) mit in das rootfs.
- Optinal könnt ihr nun alles unbenötigte löschen, bei Minern, reicht oft die eigentliche binary & der /lib ordner. `rm -fR bin/* sbin/* etc/* var/cache/* usr/share/*`

![beispiel](https://dbiesecke.github.io/images/22.png)

- Nun erstellen wir das script, was proot mit unserer passenden binary aufruft. `makeself [params] archive_dir file_name label [startup_script] [args]`

        

        makeself $PWD xmrig-self xmrig-self ./proot-x86_64 -R . /xmrig/xmrig -o de.minexmr.com:4444 [...] 


` 


