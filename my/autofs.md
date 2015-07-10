AutoFS Tips 
========================================

* Das Repo steht! ... hab den plan aber erstmal verworfen nen "all-in-one-plugin" zu bauen, zu viele abhängigkeits probleme.   ... mir repo wird alles einfacher ;)



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
