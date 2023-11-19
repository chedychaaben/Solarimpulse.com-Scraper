import requests
from bs4 import BeautifulSoup

url = "https://solarimpulse.com/companies/greenspector"

r = requests.get(url)

with open ('greenspector.html', 'w', encoding='utf-8') as f:
    f.write(r.text)