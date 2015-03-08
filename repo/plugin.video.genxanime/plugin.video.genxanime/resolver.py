import requests, re, xbmc

class resolvers:
  def streamcloud(self,url):
	try:
	  s = requests.Session()
	  content = s.get(url).content
	  data = {}
	  for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)"', content):
	    data[i.group(1)] = i.group(2).replace('download1','download2')
	  content = s.post(url, data=data).content
	  file = re.findall('file: "(.*?)"', content)[0]
	  r = requests.get(file, stream=True)
	  type = r.headers.get('content-type')
	  if type == 'video/mp4':
	    stream = file
	    return stream
	except:
	  return

  def shared(self,url):
	try:
	  content = requests.get(url).content
	  data = {}
	  r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)"', content)
	  for name, value in r:
	    data[name] = value
	  content = requests.post(url, data=data).content
	  file = re.findall('data-url="(.*?)"', content)[0]
	  r = requests.get(file, stream=True)
	  type = r.headers.get('content-type')
	  if type == 'video/mp4':
	    stream = file
	    return stream
	except:
	  return

  def novamov(self,url):
	try:
	  content = requests.get(url).content
	  r = re.search('flashvars.file="(.+?)".+?flashvars.filekey="(.+?)"', content, re.DOTALL)
	  filename, filekey = r.groups()
	  api = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s&pass=undefined&user=undefined&codes=1' % (filekey, filename)
	  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3)'}
	  content = requests.get(api, headers=headers).content
	  r = re.search('url=(.+?)&title', content)
	  file = r.group(1)
	  r = requests.get(file, stream=True)
	  type = r.headers.get('content-type')
	  if type == 'application/octet-streams':
	    stream = file
	    return stream
	except:
	  return

  def vidzi(self,url):
	try:
	  content = requests.get(url).content
	  file = re.findall('file: "(.+?mp4)"', content)[0]
	  r = requests.get(file, stream=True)
	  type = r.headers.get('content-type')
	  if type == 'application/octet-stream':
	    stream = file
	    return stream
	except:
	  return

  def primeshare(self,url):
	try:
	  s = requests.Session()
	  hash = url.split('/')[-1]
	  data = {'hash': hash}
	  headers = {'Referer': url}
	  r = s.get(url)
	  xbmc.sleep(8000)
	  content = s.post(url, data=data, headers=headers).content
	  file = re.findall("clip.*?url: '(.+?)'", content, re.DOTALL)[0]
	  r = requests.get(file, stream=True)
	  type = r.headers.get('content-type')
	  if type == 'video/mp4':
	    stream = file
	    return stream
	except:
	  return

  def vivo(self,url):
	try:
	  s = requests.Session()
	  content = s.get(url).content
	  data = {}
	  for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)"', content):
	    data[i.group(1)] = i.group(2)
	  content = s.post(url, data=data).content
	  file = re.findall('data-url="(.*?)"', content)[0]
	  r = requests.get(file, stream=True)
	  type = r.headers.get('content-type')
	  if type == 'video/mp4':
	    stream = file
	    return stream
	except:
	  return