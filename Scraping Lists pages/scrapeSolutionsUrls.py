from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd


# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Make sure you have the Chrome WebDriver installed and its location in your PATH

try :
    df = pd.read_csv('SolutionsUrls.csv')
    last_page = int(df.iloc[-1]['Page'])
except:
    df = pd.DataFrame ({
        'Page' : [],
        'ItemNumber' : [],
        'URL' : []
    })
    last_page = 0

print('Last page', last_page)

for pageNumber in range(last_page+1,43):
    print('Page', pageNumber)
    # Make a request
    driver.get(f"https://solarimpulse.com/solutions-explorer?production_si_SOLUTIONS%5Bpage%5D={pageNumber}")  # Replace "https://example.com" with your desired URL

    # Wait for 2 seconds
    time.sleep(2)

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the scroll to finish (optional)
    # You can adjust the time according to your needs
    time.sleep(2)

    # Get the page source
    page_source = driver.page_source


    soup = BeautifulSoup(page_source ,'html.parser')



    Items = soup.find('div', {'id' : 'algolia-hits'}).find('ol').find_all('li', {'class':'ais-Hits-item'})

    pageNumbers = []
    iss = []
    urls = []
    for i in range(len(Items)):
        Item = Items[i]
        pageNumbers.append(pageNumber)
        iss.append(i+1)
        urls.append(Item.find('a')['href'])

    new_rows = pd.DataFrame({
    'Page': pageNumbers,
    'ItemNumber': iss,
    'URL': urls
    })

    combined_df = pd.concat([df, new_rows], ignore_index=True)
    df = combined_df
    df.to_csv('SolutionsUrls.csv', index=False)
# Close the browser
driver.quit()