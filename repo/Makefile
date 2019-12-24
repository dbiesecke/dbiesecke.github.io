
# CFLAGS =  -Wall -g -O2 -lkeyutils -fno-omit-frame-pointer -std=c99   # -D_REENTRANT
# CSRC = $(wildcard src/*.c)
# OBJDIR = obj
# COBJS = $(patsubst src/%.c, $(OBJDIR)/%.o, $(CSRC))
# LIBFLAGS = -L$(BINDIR) -lhello -lhotpatch

ZIPS = $(wildcard */*.zip)
BLA = (plugin.video.iptvsimple.addons script.trakt plugin.video.xstream plugin.video.openmeta plugin.video.gdrive pvr.iptvsimple pvr.zattoo plugin.video.lastship)

all: build commit

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

	
	
sync:
	@test -d kdc || mkdir kdc 
	@echo start sync...
	@cd kdc && lftp -e 'set mirror:exclude-regex "PsycoTV"; mirror -c;exit' 'https://kdc-repo.website/repo-beta/Addons/' 
	@echo unzip it...
	@unzip -o "kdc/*" >/dev/null

build:  
	python repo_prep.py
	
commit: 
	git add . --all 
	git commit -a -m "new addons" && git push --all
