#!/bin/bash
echo '# Stats'
echo '========'
find . -iname "*.zip" -exec basename "{}" \; | sort | uniq | awk -F'-' '{print $1}' | 
echo ''
echo ''
echo 'IPTV Streams' $(cat plugin.video.iptvsimple.addons/resources/streams.m3u8| grep -v '#' | wc -l)
echo 'Video Addons (Repo):' $(find . -iname "*.zip" | grep "plugin.video" | wc -l)
echo 'Module (Repo):' $(find . -iname "*.zip" | grep "script.modu" | wc -l)
make icon >/dev/null 2>/dev/null
cat icons.md
echo ''
echo ''
echo '# Packages'
echo '========'
echo ''
echo ''
echo '| Packages                      | Version                 | URL                                                                                            |' 
echo '|-------------------------------|-------------------------|------------------------------------------------------------------------------------------------|' 
find . -iname "*.zip" -exec basename "{}" \; | sort | uniq | awk -F'-' '{print "| !["$1"](https://dbiesecke.github.io/repo/icons/"$1".png) "$1"\t\t| "$2" | ["$1"](https://dbiesecke.github.io/repo/"$1"/"$1"-"$2") |"}' 

