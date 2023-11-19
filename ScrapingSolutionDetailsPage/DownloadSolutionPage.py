import requests
from bs4 import BeautifulSoup

url = "https://solarimpulse.com/solutions-explorer/plastalyst-1?queryID=1e02698fc2accf12939c47b369380ada"

r = requests.get(url)

with open ('plastalyst.html', 'w', encoding='utf-8') as f:
    f.write(r.text)