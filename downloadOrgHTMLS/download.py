import httpx, re, time
import pandas as pd
from bs4 import BeautifulSoup


orgDF = pd.read_csv('../Scraping Lists pages/AllianceUrls.csv')
orgURLS = orgDF['URL']

failed_ones = []
def getHtmlPage(orgIdURL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    r = httpx.get(f'https://solarimpulse.com/{orgIdURL}', headers=headers)
    if r.status_code == 200:
        if '/companies/' in orgIdURL:
            orgIdURL = orgIdURL.replace('/companies/','')

        with open(f'htmls/{orgIdURL}.html', 'a', encoding='utf-8') as f:
            f.write(r.text)

        return 'ok'
    else:
        print('ERROR at ', orgIdURL)
        time.sleep(5)
        failed_ones.append(orgIdURL)

for i in range(len(orgURLS)):
    this_org_url = orgURLS[i]
    
    if '/companies/' in this_org_url :
        organizationID = this_org_url.replace('/companies/','')
    else:
        organizationID = ''

    with open(f'htmls/{organizationID}.html', 'r', encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        soup.find('h1', {'class': 'title title-h1 left-marker reveal-block'}).text.replace('Member - ', '')
        this_was_ok = True
    except:
        this_was_ok = False
    
    if not this_was_ok :
        print(i, this_org_url)
        getHtmlPage(this_org_url)

print(failed_ones)