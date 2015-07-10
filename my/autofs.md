AutoFS Tips 
========================================

* AutoFS erlaubt euch direkt im dateisystem "magic" like:  `ls /smb/<hostname>/` oder `ls /misc/myproject`.
  um das wieder ausmounten kümmert sich autoFS. Die Settings erlauben auch ein "lag-freies" arbeiten direkt im Desktop ;)



(secure) Mount server mit fstab & sshfs
---------------------------------------------

* Nicht sonderlich performant, aber für remote server def. ne gangbare lösung, hier ein beispiel an hidrive.
* Danach nur noch ssh-keys austauschen `ssh-copy-id USER@sftp.hidrive.strato.com`
* ACHTUNG: erlaubt "allow_other" limitiert auf userid 1000:1000, bite anpassen!


    # /etc/fstab: static file system information.
    #
    # file system      mount point    type     options                  dump pass
    /dev/xvda3         /              ext3     barrier=0                0    0
    USER@sftp.hidrive.strato.com:/public/  /misc/hidrive  fuse.sshfs noauto,x-systemd.automount,_netdev,user,idmap=user,transform_symlinks,identityfile=/root/.ssh/id_rsa,allow_other,default_permissions,uid=1000,gid=1000 0 0
    USER@sftp.hidrive.strato.com:/users/bohal/ds-2_00113215981F/  /misc/private  fuse.sshfs noauto,x-systemd.automount,_netdev,user,idmap=user,transform_symlinks,identityfile=/root/.ssh/id_rsa,allow_other,default_permissions,uid=1000,gid=1000 0 0



AutoFS - Einzelnen Remote Server anlegen
----------------------------------

* Dafür wird typischerweise der `/misc` ordner verwendet, darauf folgt euer gewünschter name.

/etc/auto.misc:

    myproject  -rw,soft,intr,rsize=8192,wsize=8192 nfs.example.net:/proj52
    
* **Hint: UDP verbessert massiv die performence dafür wie folgt anhängen: `,wsize=8192,udp`


    myproject  -rw,soft,intr,rsize=8192,wsize=8192,udp nfs.example.net:/proj52


auto.master config
----------------------------------

Main config file, invoke the bashscript as "invoker"


    #
    # Sample auto.master file
    # This is an automounter map and it has the following format
    # key [ -mount-options-separated-by-comma ] location
    # For details of the format look at autofs(5).
    #
    /misc   /etc/auto.misc
    #
    # NOTE: mounts done from a hosts map will be mounted with the
    #       "nosuid" and "nodev" options unless the "suid" and "dev"
    #       options are explicitly given.
    #
    /net -hosts --timeout=60
    /smb            /etc/auto.ftp      --timeout=60
    /media/net      /etc/auto.net      --timeout=60



auto.smb invoker
----------------------------------

Main config file, invoke the bashscript as "invoker"
from now you can acces remote SMB server like:  `ls /smb/<hostname>/`




    #!/bin/bash
    
    # This file must be executable to work! chmod 755!
    
    key="$1"
    opts="-fstype=cifs"
    
    for P in /bin /sbin /usr/bin /usr/sbin
    do
    	if [ -x $P/smbclient ]
    	then
    		SMBCLIENT=$P/smbclient
    		break
    	fi
    done
    
    [ -x $SMBCLIENT ] || exit 1
    
    $SMBCLIENT -gNL $key 2>/dev/null| awk -v key="$key" -v opts="$opts" -F'|' -- '
    	BEGIN	{ ORS=""; first=1 }
    	/Disk/	{
    		  if (first)
    			print opts; first=0
    		  dir = $2
    		  loc = $2
    		  # Enclose mount dir and location in quotes
    		  # Double quote "$" in location as it is special
    		  gsub(/\$$/, "\\$", loc);
    		  gsub(/\&/,"\\\\&",loc)
    		  print " \\\n\t \"/" dir "\"", "\"://" key "/" loc "\""
    		}
    	END 	{ if (!first) print "\n"; else exit 1 }
    	'
    



auto.net (NFS) Invoker
----------------------------------

from now you can acces remote NFS server like:  `ls /media/net/<hostname>/`


    
    #!/bin/bash
    
    # This file must be executable to work! chmod 755!
    
    # Look at what a host is exporting to determine what we can mount.
    # This is very simple, but it appears to work surprisingly well
    
    key="$1"
    
    # add "nosymlink" here if you want to suppress symlinking local filesystems
    # add "nonstrict" to make it OK for some filesystems to not mount
    # choose one of the two lines below depending on the NFS version in your
    # environment
    opts="-fstype=nfs,hard,intr,nodev,nosuid"
    #opts="-fstype=nfs4,hard,intr,nodev,nosuid,async"
    
    # Showmount comes in a number of names and varieties.  "showmount" is
    # typically an older version which accepts the '--no-headers' flag
    # but ignores it.  "kshowmount" is the newer version installed with knfsd,
    # which both accepts and acts on the '--no-headers' flag.
    #SHOWMOUNT="kshowmount --no-headers -e $key"
    #SHOWMOUNT="showmount -e $key | tail -n +2"
    
    for P in /bin /sbin /usr/bin /usr/sbin
    do
    	for M in showmount kshowmount
    	do
    		if [ -x $P/$M ]
    		then
    			SMNT=$P/$M
    			break
    		fi
    	done
    done
    
    [ -x $SMNT ] || exit 1
    
    # Newer distributions get this right
    SHOWMOUNT="$SMNT --no-headers -e $key"
    
    $SHOWMOUNT | LC_ALL=C cut -d' ' -f1 | LC_ALL=C sort -u | \
    	awk -v key="$key" -v opts="$opts" -- '
    	BEGIN	{ ORS=""; first=1 }
    		{ if (first) { print opts; first=0 }; print " \\\n\t" $1, key ":" $1 }
    	END	{ if (!first) print "\n"; else exit 1 }
    	' | sed 's/#/\\#/g'
