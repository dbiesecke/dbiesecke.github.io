# -*- coding: utf-8 -*-

import requests, re, xbmc, urllib
from resources.lib import common

timeout = common.get_timeout()

def get_file(hoster_list):
    file = ''
    for hoster in hoster_list:
        for link in hoster:
            if 'vidzi' in link and not file:
                file = vidzi(link)
            elif 'vivo' in link and not file:
                file = vivo(link)
            elif 'streamcloud' in link and not file:
                file = streamcloud(link)
            elif 'shared' in link and not file:
                file = shared(link)
            elif 'novamov' in link and not file:
                file = novamov(link)
            elif 'primeshare' in link and not file:
                file = primeshare(link)
            elif 'anime-tube' in link and not file:
                file = animetube(link)
            elif 'divxstage' in link and not file:
                file = divxstage(link)
            elif 'myvideo' in link and not file:
                file = myvideo(link)
            elif 'clipfish' in link and not file:
                file = clipfish(link)
            elif 'youtube' in link and not file:
                file = youtube(link)
            elif 'crunchyroll' in link and not file:
                file = crunchyroll(link)
            elif 'viewster' in link and not file:
                file = viewster(link)
            elif not file: 
                file = check_file_type(link)
    return file

def check_file_type(file):
    try:
        r = requests.head(file, timeout=timeout)
        type = r.headers.get('content-type')
        if type == 'video/mp4' or type == 'application/octet-stream' or type == 'application/x-mpegurl':
            return file
    except:
        pass
    
def streamcloud(url):
    try:
        s = requests.Session()
        content = s.get(url, timeout=timeout).content
        data = {}
        for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)"', content):
            data[i.group(1)] = i.group(2).replace('download1','download2')
        content = s.post(url, data=data).content
        file = re.findall('file: "(.*?)"', content)[0]
        file = check_file_type(file)
        if file: return file
    except:
        pass

def shared(url):
    try:
        content = requests.get(url, timeout=timeout).content
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)"', content)
        for name, value in r:
            data[name] = value
        content = requests.post(url, data=data, timeout=timeout).content
        file = re.findall('data-url="(.*?)"', content)[0]
        file = check_file_type(file)
        if file: return file
    except:
        pass

def novamov(url):
    try:
        content = requests.get(url, timeout=timeout).content
        r = re.search('flashvars.file="(.+?)".+?flashvars.filekey="(.+?)"', content, re.DOTALL)
        filename, filekey = r.groups()
        api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s&pass=undefined&user=undefined&codes=1' % (filekey, filename)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3)'}
        content = requests.get(api, headers=headers, timeout=timeout).content
        r = re.search('url=(.+?)&title', content)
        file = r.group(1)
        file = check_file_type(file)
        if file: return file
    except:
        pass

def vidzi(url):
    try:
        content = requests.get(url, timeout=timeout).content
        file = re.findall('file: "(.+?mp4)"', content)[0]
        file = check_file_type(file)
        if file: return file
    except:
        pass

def divxstage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3)', 'Host': 'www.divxstage.to'}
        api_url = 'http://www.divxstage.to/api/player.api.php?key=%s&file=%s'
        content = requests.get(url, timeout=timeout).content
        _file = re.findall('file="(.+?)"', content)[0]
        _key = re.findall('filekey="(.+?)"', content)[0]
        content = requests.get(api_url % (_key,_file), headers=headers, timeout=timeout).content
        file = re.findall('url=(.+?)&', content)[0]
        file = check_file_type(file)
        if file: return file
    except:
        pass
        
def primeshare(url):
    try:
        s = requests.Session()
        hash = url.split('/')[-1]
        data = {'hash': hash}
        headers = {'Referer': url}
        content = s.get(url, timeout=timeout).content
        if re.search('>File not exist<', content): return
        xbmc.sleep(8000)
        content = s.post(url, data=data, headers=headers).content
        file = re.findall("clip.*?url: '(.+?)'", content, re.DOTALL)[0]
        file = check_file_type(file)
        if file: return file
    except:
        pass

def vivo(url):
    try:
        s = requests.Session()
        content = s.get(url, timeout=timeout).content
        data = {}
        for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)"', content):
            data[i.group(1)] = i.group(2)
        content = s.post(url, data=data).content
        file = re.findall('data-url="(.*?)"', content)[0]
        file = check_file_type(file)
        if file: return file
    except:
        pass
        
def animetube(url):
    try:
        content = requests.get(url, timeout=timeout).content
        link = re.findall('(http://.*?ani-stream.com/.*?.html)', content)[0]
        content = requests.get(link, timeout=timeout).content
        file = re.findall("file: '(.+?)'", content)[0]
        try:
            r = requests.head(file, timeout=timeout)
            location = r.headers.get('location')
            if location:
                file = location
        except:
            pass
        file = check_file_type(file)
        if file: return file
    except:
        pass
        
def myvideo(url):
    try:
        try: vid = re.findall(r'/(\d+)', url)[-1]
        except: vid = re.findall(r'\d+', url)[-1]
        # thx to bromix for headers and api url
        headers = {'Accept-Language': 'en_US',
                    'X-PAPI-AUTH': '39927b3f31d7c423ad6f862e63d8436d954aecd0',
                    'Host': 'papi.myvideo.de',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Not set yet'}
        api_url = 'https://papi.myvideo.de/myvideo-app/v1/vas/video.json?clipid=%s&app=megapp&method=4' % vid
        json_data = requests.get(api_url, headers=headers, timeout=timeout).json()
        file = json_data['VideoURL']
        file = check_file_type(file)
        if file: return file
    except:
        pass
    
def clipfish(url):
    try:
        vid = re.findall(r'/(\d+)/', url)[0]
        api_url = 'http://www.clipfish.de/devapi/id/%s?format=json&apikey=hbbtv' % vid
        json_data = requests.get(api_url, timeout=timeout).json()
        file = json_data['items'][0]['media_videourl']
        file = check_file_type(file)
        if file: return file
    except:
        pass
        
def youtube(url):
    try:
        vid = re.findall(r'v=([^&]+)', url)[0]
        return 'plugin://plugin.video.youtube/play/?video_id=' + vid
    except:
        pass
        
def viewster(url):
    try:
        vid = re.findall(r'/movie/(.+?)/', url)[0]
        # thx to learningit for parts of the code
        json_data = requests.get('http://api.live.viewster.com/api/v1/movie/%s' % vid, timeout=timeout).json()
        for a in json_data['play_list']:
            if a['autoplay'] == True:
                break
        a =  a['link_request']
        params = urllib.urlencode(a)
        headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X)'}
        json_data = requests.get('http://api.live.viewster.com/api/v1/MovieLink?%s' % params, headers=headers, timeout=timeout).json()
        file = json_data['url']
        return file
    except:
        pass
        
def crunchyroll(url):
    try:
        # thx to thevladsoft for parts of the code
        from resources.lib.decoder import CrunchyDecoder
        url = url.split('?')[0]
        subtitle = common.get_subtitle()
        xml_url = 'http://www.crunchyroll.com/xml/'
        media_id = url[-6:]
        s = requests.Session()
        content = s.get(url).content
        player_revision = re.findall(r'flash\\/(.+)\\/StandardVideoPlayer.swf', content)[0]
        headers = {'Referer':'http://static.ak.crunchyroll.com/flash/' + player_revision + '/StandardVideoPlayer.swf', 'Host':'www.crunchyroll.com', 'Content-type':'application/x-www-form-urlencoded', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'}
        data = {'req': 'RpcApiVideoPlayer_GetStandardConfig', 'media_id': media_id,
                'video_format': '106', 'video_quality': '61', 'auto_play': '1',
                'show_pop_out_controls': '1', 'current_page': 'http://www.crunchyroll.com/'}
        content = s.post(xml_url, headers=headers, data=data).content
        host = re.findall('<host>(.+?)</host>', content)[0]
        token = re.findall('<token>(.+?)</token>', content)[0]
        file = re.findall('<file>(.+?)</file>', content)[0]
        subtitles = re.findall("<subtitle id='(.+?)'.*?user='(.+?)'", content)
        for subtitle_id, user in subtitles:
            if user == 'cr_de': subtitle_id = subtitle_id
        rtmp_url = host.replace('&amp;','&') + " swfurl=" +"http://static.ak.crunchyroll.com/flash/"+player_revision+"/ChromelessPlayerApp.swf" + " swfvfy=1 token=" +token+ " playpath=" +file.replace('&amp;','&')+ " pageurl=" +url
        data = {'req': 'RpcApiSubtitle_GetXml', 'subtitle_script_id': subtitle_id}
        content = s.post(xml_url, headers=headers, data=data).content
        formattedSubs = CrunchyDecoder().return_subs(content)
        fh = open(subtitle, 'w')
        fh.write(formattedSubs.encode('UTF-8'))
        fh.close()
        return rtmp_url
    except:
        pass