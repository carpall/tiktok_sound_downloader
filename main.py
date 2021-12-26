import requests

from bs4 import BeautifulSoup
from os import system, walk, getcwd

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
}

tikTokDomains = (
    'http://vt.tiktok.com', 'http://app-va.tiktokv.com', 'http://vm.tiktok.com', 'http://m.tiktok.com', 'http://tiktok.com', 'http://www.tiktok.com', 'http://link.e.tiktok.com', 'http://us.tiktok.com',
    'https://vt.tiktok.com', 'https://app-va.tiktokv.com', 'https://vm.tiktok.com', 'https://m.tiktok.com', 'https://tiktok.com', 'https://www.tiktok.com', 'https://link.e.tiktok.com', 'https://us.tiktok.com'
)

def getToken(url):
  try:
    response = requests.post('https://musicaldown.com/', headers=headers)
        
    cookies = response.cookies
    soup = BeautifulSoup(response.content, 'html.parser').find_all('input')

    data = {
      soup[0].get('name'): url,
      soup[1].get('name'): soup[1].get('value'),
      soup[2].get('name'): soup[2].get('value')
    }
    
    return True, cookies, data

  except Exception:
    return None, None, None

def getVideo(url):
  if not url.startswith('http'):
    url = 'https://' + url

  if not url.lower().startswith(tikTokDomains):
    return {
      'success': False,
      'error': 'invalidUrl'
    }
    
  url = url.split('?')[0]
    
  status, cookies, data = getToken(url)

  if not status:
    return {
      'success': False,
      'error': 'exception'
    }

  headers = {
    'Cookie': f"session_data={cookies['session_data']}",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '96',
    'Origin': 'https://musicaldown.com',
    'Referer': 'https://musicaldown.com/en/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Te': 'trailers'
  }

  try:
    response = requests.post('https://musicaldown.com/download', data=data, headers=headers, allow_redirects=False)

    if 'location' not in response.headers:
      soup = BeautifulSoup(response.content, 'html.parser')

      return {
        'success': True,
        'type': 'video',
        'description': soup.findAll('h2', attrs={'class':'white-text'})[0].get_text()[23:-19],
        'thumbnail': soup.findAll('img',attrs={'class':'responsive-img'})[0]['src'],
        'link': soup.findAll('a',attrs={'class':'btn waves-effect waves-light orange'})[3]['href'],
        'url': url
      }
    
    if response.headers['location'] == '/en/?err=url invalid!':
      return {
        'success': False,
        'error': 'invalidUrl'
      }

    elif response.headers['location'] == '/en/?err=Video is private!':
      return {
        'success': False,
        'error': 'privateVideo'
      }

    elif response.headers['location'] == '/mp3/download':
      response = requests.post('https://musicaldown.com//mp3/download', data=data, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')

      return {
        'success': True,
        'type': 'audio',
        'description': soup.findAll('h2', attrs={'class':'white-text'})[0].get_text()[13:],
        'thumbnail': None,
        'link': soup.findAll('a', attrs={'class':'btn waves-effect waves-light orange'})[3]['href'],
        'url': url
      }

    else:
      return {
        'success': False,
        'error': 'unknownError'
      }

  except Exception:
      return {
          'success': False,
          'error': 'exception'
      }

def clear():
  system('cls')

choose = input('file or url? [f/u]: ')

urls = open(input('file: ')).readlines() if choose == 'f' else input('url: ')

clear()

file_count = 0

for file in walk(getcwd()):
  break

if len(file) >= 3:
  files = file[2]

  for file in files:
    if file.startswith('audio'):
      file_count += 1

for i, url in enumerate(urls):
  print(f'{i}/{len(urls)}')

  url = getVideo(url)['link']
  mp3 = requests.get(url)

  with open(f'audio{i + file_count}.mp3', 'wb') as f:
    f.write(mp3.content)
  
  clear()

print('finished')
