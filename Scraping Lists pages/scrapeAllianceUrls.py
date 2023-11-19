import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame ({
    'Page' : [],
    'ItemNumber' : [],
    'URL' : []
})

counter = 0


for pageNumber in range(1,194):
    print('Page', pageNumber)
    url = f"https://solarimpulse.com/alliance-network?filter=all&page={pageNumber}"

    r = requests.get(url)

    soup = BeautifulSoup(r.text,'html.parser')

    infoNetwork = soup.find_all('div', {'id':'info-network'})[0]


    Items = infoNetwork.find('div', {'id' : 'results'}).find('ul').find_all('li', {'class':'reveal-block'})

    for i in range(len(Items)):
        Item = Items[i]
        df.loc[counter] = [pageNumber, i+1, Item.find('a')['href']]
        counter += 1



df.to_csv('AllianceUrls.csv', index=False)