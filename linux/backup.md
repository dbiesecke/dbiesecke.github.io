# BackUp - Notes & Tips
- - - - - - - - - - - - - - - 

Disaster recovery easy with rear
------------------------------
* on Debian based system ( also Ubutnu etc) use this dpkg package: [rear_1.17.2_all.deb](/rear_1.17.2_all.deb)
* Out-of the box muss nur eingestellt werden, was für recovery image ihr erstelen wollt.
* Bsp 1: OUTPUT=USB && BACKUP_URL=usb:///dev/disk/by-label/REAR-000 ersellt ein bootfähiges USB medium mit allen benötigen daten zum wiederherstellen
* Note: Vorher muss das USB msedium per `$ rear format /dev/sdX` komplett platt gemacht werden, danach können die Partitionen ja geresized werden 

* Mehr infos auf [backupinferno](http://backupinferno.de/?p=358)


