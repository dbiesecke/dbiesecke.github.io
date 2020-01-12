
# CFLAGS =  -Wall -g -O2 -lkeyutils -fno-omit-frame-pointer -std=c99   # -D_REENTRANT
# CSRC = $(wildcard src/*.c)
# OBJDIR = obj
# COBJS = $(patsubst src/%.c, $(OBJDIR)/%.o, $(CSRC))
# LIBFLAGS = -L$(BINDIR) -lhello -lhotpatch
PWD = $(pwd)
ZIPS = $(wildcard */*.zip)
BLA = (plugin.video.iptvsimple.addons script.trakt plugin.video.xstream plugin.video.openmeta plugin.video.gdrive pvr.iptvsimple pvr.zattoo plugin.video.lastship)

all: build

backup_external:

	#scp -r libre.lan:.config/system.d _OS
	scp -r libre.lan:.kodi/userdata/addon_data/ ./_OS/
	scp -r libre.lan:.kodi/addons/ ./_OS/addons/
	
	#scp -r libre.lan:.kodi/userdata/
	#for i in $BLA; do  ;done



publish:
	find . -maxdepth 2 -iname "*.zip" | grep "script" | parallel -j2 rsync -cvr  "{}" bohal@rsync.hidrive.strato.com:/public/XBMC/KODi-MODULE/
	find . -maxdepth 2 -iname "*.zip" | grep "repository" | parallel -j2 rsync -cvr  "{}" bohal@rsync.hidrive.strato.com:/public/XBMC/KODI-REPOS/
	find . -maxdepth 2 -iname "*.zip" | grep "plugin" | parallel -j2 rsync -cvr  "{}" bohal@rsync.hidrive.strato.com:/public/XBMC/KODI-ADDONS/

index:
	@./filelist.sh
	
convert-icons:

	
sync:
	@test -d kdc || mkdir kdc 
	@echo start sync...
	@cd kdc && lftp -e 'set mirror:exclude-regex "PsycoTV"; mirror -c;exit' 'https://kdc-repo.website/repo-beta/Addons/' 
	@echo unzip it...
	@unzip -o "kdc/*" >/dev/null

icons:
	@test -d icons || mkdir icons
	@find . -maxdepth 1 -iname "*.*" | sort | parallel cp "{}/icon.png" "icons/{}.png"	2>/dev/null ; echo
	@find . -iname "icon*.png" -exec cp "{}"  "{}.bak" \; 2>/dev/null ; echo
	@find . -iname "icon*.png" -exec convert -resize 32x32 "{}.bak" "{}" \; 2>/dev/null ; echo
	@find . -iname "icon*.bak" -delete 2>/dev/null ; echo
	
icon: icons convert-icons

	@find ./icons/ -iname "*video*" -exec basename "{}" \; | awk  '{print " !["$$1"](https://dbiesecke.github.io/repo/icons/"$$1")"}' 

build:  icon
	@find . -maxdepth 2 -iname "*.pyo" -delete 
	@rsync -r ./* ./build/ ; echo true
	@cd build && python ./repo_prep.py ; cd ..
	@rsync -cvr ./build/* .
	find . -maxdepth 2 -iname "*.zip" 
	@rm -fR build
	@bash ./filelist.sh > index.md

commit: 
	git add . --all 
	git commit -a -m "new addons" && git push --all
