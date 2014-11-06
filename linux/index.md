# Usefull Notes
- - - - - - 


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

