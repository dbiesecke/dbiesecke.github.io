#!/bin/bash
#rm -fR ./zips/*
python ./repo_prep.py
cp ./*/*.zip ./zips/
cp ./*/*md5 ./zips/

rsync -r ./* root@ds-2:/volume1/web/repo/

