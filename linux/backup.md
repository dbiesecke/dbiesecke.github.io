
# BackUp - Notes & Tips
- - - - - - - - - - - - - - - 

Disaster recovery easy with rear
------------------------------
* on Debian based system ( also Ubutnu etc) use this dpkg package: [rear_1.17.2_all.deb](/rear_1.17.2_all.deb)
* Out-of the box muss nur eingestellt werden, was für recovery image ihr erstelen wollt.

      $ sudo cat /etc/rear/local.conf
      this_file_name=$( basename ${BASH_SOURCE[0]} )
      LOGFILE="$LOG_DIR/rear-$HOSTNAME-$WORKFLOW-${this_file_name%.*}.log"
      BACKUP_PROG_EXCLUDE=( "${BACKUP_PROG_EXCLUDE[@]}" '/home/*' '/src/*' '/opt/cross/*' )
      BACKUP_PROG_ARCHIVE="backup-${this_file_name%.*}"
      BACKUP=NETFS
      BACKUP_OPTIONS="nfsvers=3,nolock,udp"
      BACKUP_URL=nfs://192.168.1.100/volume1/backup/rear/main
      $ sudo rear mkbackup
      


* Bsp 1: `$ OUTPUT=USB && BACKUP_URL=usb:///dev/disk/by-label/REAR-000 sudo mkbackup` ersellt ein bootfähiges USB medium mit allen benötigen daten zum wiederherstellen
* Note: Vorher muss das USB msedium per `$ rear format /dev/sdX` komplett platt gemacht werden, danach können die Partitionen ja geresized werden 





