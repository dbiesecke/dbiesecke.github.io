#!/bin/bash
rm -fR ./zips/*
python ./repo_prep.py
cp ./*/*.zip ./zips/
rsync -r ./* root@ds-2:/volume1/web/repo/

