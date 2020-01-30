
# CFLAGS =  -Wall -g -O2 -lkeyutils -fno-omit-frame-pointer -std=c99   # -D_REENTRANT
# CSRC = $(wildcard src/*.c)
# OBJDIR = obj
# COBJS = $(patsubst src/%.c, $(OBJDIR)/%.o, $(CSRC))
# LIBFLAGS = -L$(BINDIR) -lhello -lhotpatch
PWD = $(pwd)
ZIPS = $(wildcard */*.zip)
BLA = (plugin.video.iptvsimple.addons script.trakt plugin.video.xstream plugin.video.openmeta plugin.video.gdrive pvr.iptvsimple pvr.zattoo plugin.video.lastship)
ITEM = metadata.common.theaudiodb.com

all: commit

item:
# 	@echo '<item>'
# 	@echo '                        <label>Install: Scraper - '$(ITEM)'</label>'
# 	@echo '                        <onclick>InstallAddon('$(ITEM)')</onclick>'
# 	@echo '                        <visible>!System.HasAddon('$(ITEM)')</visible>'
# 	@echo '</item>'
	@echo '<item>'
	@echo '                        <label>Scraper - '$(ITEM)' $$INFO[System.AddonVersion('$(ITEM)'),(,)]</label>'
	@echo '                        <onclick>Addon.OpenSettings('$(ITEM)')</onclick>'
	@echo '                        <visible>System.HasAddon('$(ITEM)')</visible>'
	@echo '</item>'
	
item-list.xml:
	@for i in $$(cat plugin-list); do make item ITEM=$$i >>./item-list.xml;done
	
skin-sync:
	@test -d skin.horizonzv.test/1080p/ && cp -R skin.horizonzv.test/1080p/* ~/.kodi/addons/skin.horizonzv.test/1080p/
	@pidof kodi || kodi &
kate:
	kate -l 281 -b skin.horizonzv.test/1080p/Includes_SidePanel_right.xml skin.horizonzv.test/1080p/Custom_1800_UsedAddons.xml skin.horizonzv.test/1080p/Home.xml Makefile 2>/dev/null &
# 	kate -l 181 -b skin.horizonzv.test/1080p/Custom_1800_UsedAddons.xml  2>/dev/null &
# 	kate -l 387 -b skin.horizonzv.test/1080p/Home.xml  2>/dev/null &

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

remove-index:
	@test -f index.md || rm index.md 2>/dev/null 
	
index.md:
	@./filelist.sh > index.md
	
rebuild: rebuild-remove remove-index build

rebuild-remove:
	@test -f skin.horizonzv.test/skin.horizonzv.test-*.zip || rm -fR skin.horizonzv.test/skin.horizonzv.test-*.zip
	@test -f skin.horizonzv.test/changelog-* || rm -fR skin.horizonzv.test/changelog-*
	
	
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
	@find . -iname "icon*.png" -exec convert -resize 64x64 "{}.bak" "{}" \; 2>/dev/null ; echo
	@find . -iname "icon*.bak" -delete 2>/dev/null ; echo
	
icon: icons 
	@echo 'Plugins' > icons.md
	@echo '=========' >> icons.md
	@echo ''>> icons.md
	@echo 'Video Addons' >> icons.md
	@echo ''>> icons.md
	@find ./icons/ -iname "*video*" -exec basename "{}" \; | awk  '{print " !["$$1"](https://dbiesecke.github.io/repo/icons/"$$1")"}' >> icons.md
	@echo ''>> icons.md
	@echo 'Program Addons' >> icons.md
	@echo ''>> icons.md
	@find ./icons/ -iname "*program*" -exec basename "{}" \; | awk  '{print " !["$$1"](https://dbiesecke.github.io/repo/icons/"$$1")"}' >> icons.md
	@echo ''>> icons.md
	@echo 'Repos' >> icons.md
	@echo ''>> icons.md
	@find ./icons/ -iname "repository*" -exec basename "{}" \; | awk  '{print " !["$$1"](https://dbiesecke.github.io/repo/icons/"$$1")"}' >> icons.md
	@echo ''>> icons.md
	@echo 'Module' >> icons.md
	@echo ''>> icons.md
	@find ./icons/ -iname "script.mo*" -exec basename "{}" \; | awk  '{print " !["$$1"](https://dbiesecke.github.io/repo/icons/"$$1")"}' >> icons.md	
	
build:   index.md icon 
	@find . -maxdepth 2 -iname "*.pyo" -delete 
	@rsync -r ./* ./build/ ; echo true
	@cd build && python ./repo_prep.py ; cd ..
	@rsync -cvr ./build/* . >/dev/null
#	@find . -maxdepth 2 -iname "*.zip" 
	@rm -fR build

commit: build
	git add ./*/* index.md --all 
	git commit -a -m "new addons" && git push --all
