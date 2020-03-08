import xbmc,os
import json

datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.animeanime/')
if not os.path.isdir(datapath):
    os.mkdir(datapath)
mal = os.path.join(datapath,'mal.json')

def get_my_anime_entries():
    if os.path.exists(mal):
        with open(mal) as f:
            json_data = json.load(f)
        if json_data:
            return json_data

def add_to_mal(site,id):
    entries = get_my_anime_entries()
    new_entry = {'site': site, 'id': id}
    if entries:
        for entry in entries:
            if entry['site'] == site and entry['id'] == id:
                xbmc.executebuiltin('Notification(Anime Bereits Hinzugef\xc3\xbcgt,)')
                return
        entries.append(new_entry)
        save(entries)
    else:
        save([new_entry])
    xbmc.executebuiltin('Notification(Anime Hinzugef\xc3\xbcgt,)')
 
def save(entry):
    with open(mal, 'w') as f:
        json.dump(entry, f)
        
def remove_from_mal(site,id):
    with open(mal) as f:
        json_data = json.load(f)
    for i in xrange(len(json_data)):
        if json_data[i]["site"] == site and json_data[i]["id"] == id:
            json_data.pop(i)
            break
    save(json_data)
    xbmc.executebuiltin('Notification(Anime Entfernt,)')