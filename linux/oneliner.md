Diverse Linux OneLiner
---------------------------------


App::Every
---------------------------------
Makes a cron entry with 2x simple parameters.

* Alias: `alias cron-every='curl -sk 'https://raw.githubusercontent.com/iarna/App-Every/master/packed/every' | perl -X - -n  -l'`

*  Example:

    `% cron-every 3 hours ls`


        PATH=/home/foilo/cappucino/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/home/foilo/.rvm/bin
        LOCKFILE=/tmp/every_lock_b8d65f1a8f00500bbda75fc44a4d5f88
        SHELL=/bin/zsh
        54 */3 * * * [ ! -f $LOCKFILE -o ! -d /proc/`[ -f $LOCKFILE ] && cat $LOCKFILE` ] && ( echo $$ > $LOCKFILE ; cd "/home/foilo";  ls  ; rm $LOCKFILE )


Debian GRML scripts
---------------------------------

            wget -qO- http://deb.grml.org/repo-key.asc | sudo apt-key add --    
            sudo echo   'deb     http://deb.grml.org/ grml-testing main' > /etc/apt/sources.list.d/grml.list
            sudo apt-get update 

Install some usefull tools
---------------------------------

            sudo apt-get install grml-tips grml-crypt grml-network grml-paste grml-shlib grml-tips grml-quickconfig grml-scripts
            
Install ZSH
---------------------------------

            wget -qO- .zshrc http://git.grml.org/f/grml-etc-core/etc/zsh/zshrc


Monodevelop Latest
---------------------------------

            sudo add-apt-repository ppa:keks9n/monodevelop-latest
            
Scribes
---------------------------------

            sudo add-apt-repository ppa:mystilleef/scribes-daily
