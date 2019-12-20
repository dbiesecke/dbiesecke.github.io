##/bin/zsha

BLA=$(echo plugin.video.iptvsimple.addons script.trakt plugin.video.xstream plugin.video.openmeta plugin.video.gdrive pvr.iptvsimple pvr.zattoo plugin.video.lastship)

for i in $BLA; do scp -r libre.lan:.kodi/addons/$i ./_OS/addons/$i ;done


for i in $BLA; do scp -r libre.lan:.kodi/userdata/addon_data/$i ./_OS/userdata/addon_data/$i ;done

