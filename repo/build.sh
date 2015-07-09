#!/bin/bash
#rm -fR ./zips/*
python ./repo_prep.py
cp ./*/*.zip ./zips/
cp ./*/*md5 ./zips/
perl -e 'foreach(<./*/addon.xml>){ system("md5sum $_ > $_.md5")}' && perl -e 'foreach(<./*/*.zip>){ system("md5sum $_ > $_.md5")}' && perl -e 'foreach(<./zips/*>){ system("md5sum $_ > $_.md5")}'
rsync -r ./* root@ds-2:/volume1/web/repo/

