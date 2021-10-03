import requests
import brotli
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings()

#User Profile URLs
url_List = ['https://www.upwork.com/freelancers/~01839791ddb1ede3fa']

google_form_url='https://docs.google.com/forms/d/e/******************/formResponse'


def GetPageUsingRequest(url):
    textContent = ''
    try:
        header =  { 'accept-encoding': 'gzip, deflate', 'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8,ta;q=0.7',
                   'cache-control': 'max-age=0', 'dnt': '1',	'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
                   'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'Referer': 'https://www.google.com/', 'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36' }

        session = requests.Session()
        session.max_redirects = 20
        response = session.get(url, verify=False, timeout=30, headers=header, stream=False)
        if response.status_code == 200:
            print(f'{url} load Successful')
            if response.headers.get('Content-Encoding', '') == 'br':
                textContent = brotli.decompress(response.content)
            else:
                textContent = response.text
        else:
            print(f'{url} load Failed - HTTPCode: {response.status_code}')
    except Exception as e:
        print(f'{url} load Errored')
    finally:
        session.close
    return textContent


for url in url_List:
    if url and 'upwork' in url:
        Name = Score = ""
        # scrape html from url
        if html := GetPageUsingRequest(url):
            # parse text using bs4
            if soup := BeautifulSoup(html, 'html.parser'):
                if items:= soup.find_all('h1', attrs={'itemprop': 'name'}):
                    Name = items[0].text.strip()
                if items := soup.select('h3'):
                    Score = items[0].text
                    if '%' not in Score:
                        print(f'No Job Success Score found for {Name}')
                    else:
                        Score = Score.replace('%', '')
                        print(f'{Name} Job Success Score = {Score}%')
                        gFormParams = {'entry.******' : Name, 'entry.******' : Score}
                        resp = requests.post(google_form_url, data=gFormParams, verify=False)
                        if resp.status_code == 200:
                            print('Successfully posted data to Form.')
                        else:
                            print('Error: %s' % resp.content)

