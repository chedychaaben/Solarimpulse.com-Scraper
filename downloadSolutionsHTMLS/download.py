import httpx, re
import pandas as pd


solutionsDF = pd.read_csv('../Scraping Lists pages/SolutionsUrls.csv')
solutionsUrls = solutionsDF['URL']

def getHtmlPage(solutionIdURL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    r = httpx.get(f'https://solarimpulse.com/{solutionIdURL}', headers=headers)

    if 'solutions-explorer/' in solutionIdURL:
        solutionIdURL = solutionIdURL.replace('solutions-explorer/','')
    whereisQmark = solutionIdURL.find('?')
    solutionIdURL = solutionIdURL[:whereisQmark]

    with open(f'htmls/{solutionIdURL}.html', 'a', encoding='utf-8') as f:
        f.write(r.text)

    return 'ok'

for i in range(len(solutionsUrls)):
    print(i, solutionsUrls[i])
    getHtmlPage(solutionsUrls[i])