Storage Tips & Tricks 
==========================================================
* ... or  "How to get 100TB++ for free from google"
* Die meisten Tools basieren auf dem sehr guten "rclone", dieser kommt nun auch mit WebUI daher
 
![AnkDhuE.png](https://i.imgur.com/AnkDhuE.png)


## Install
------------------------
* Install main binary  `curl https://rclone.org/install.sh | sudo bash`
* Install sprinkle from source: 


    sudo -H python3.6 -mpip install git+https://github.com/mmontuori/sprinkle.git

* Initial sollte man erstmal ein "paar" Service accounts erstellen. Dabei hilft [AutoRclone](https://github.com/xyou365/AutoRclone) & macht es so möglich ganz easy 600 accounts zu erstellen.
 
## Tools
-----------


| Name         | Key #1                                                                             | Tolls     |
|--------------|------------------------------------------------------------------------------------|-----------|
| [uds](https://github.com/stewartmcgown/uds)  |  Unlimited Storage - 0 Byte files on Google Docs   | cli/[gui](https://github.com/stewartmcgown/uds-web)    
| [AutoRclone](https://github.com/xyou365/AutoRclone)   | Get ca. 150TB Space from Google            |  CLI        
|  [sprinkle](https://github.com/mmontuori/sprinkle) |  It presents all the RClone available volumes as a single clustered volume. | CLI/SRV 


## Usage
-----------
* Automount with autofs - [rclone-fstab-mount-helper-script](https://github.com/rclone/rclone/wiki/rclone-fstab-mount-helper-script)
* Example commands


        $ rconsole ls <remote>:<path
        $ rconsole mount <remote>:<path /mnt/temp
        
        


## (Web)UI
---------------------
* Start a Webgui server 


    rclone rcd --rc-web-gui --rc-user admin --rc-pass yeah12ha --rc-addr ":5572" --rc-serve 




## Autostart / Service
-------------------------
* hier ein Ubic script was am ende keine auth verwendet (da http davor geschalten wurde) - `/etc/ubic/service/rclone/rclone`
        

    #!/usr/bin/perl -w
    
    use Ubic::Service::SimpleDaemon;
    Ubic::Service::SimpleDaemon->new(
     bin => 'rclone rcd --rc-web-gui --rc-no-auth --rc-addr "127.0.0.1:5572" --rc-serve',
     cwd => "/root",
    );


## Sprinkle
-------------------------

* Ich arbeite aktuell mit 100 (google free) accounts & [sprinkle](https://github.com/mmontuori/sprinkle) . Dieser bringt eine simples cli interface & einen daemon mit. 

        $ sprinkle.py ls /backup
        $ sprinkle.py backup /dir_to_backup
        $ sprinkle.py restore /backup /opt/restore_dir
        
![Spr8ANG.png](https://i.imgur.com/Spr8ANG.png)



 
