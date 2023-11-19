import httpx, re
from bs4 import BeautifulSoup
import pandas as pd


def getDfRow(index, solutionUrl, solutionID, html_content):
    
    # Parse the HTML into a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    name = soup.find('h1', {'class': 'title-h1'}).text

    summary = soup.find('p', {'class': 'sub-h1'}).text
    identification = soup.find('p', {'class': 'p'}).text

    # Right corner data (As they are)
    rightCornerDiv = soup.find('div', {'class': 'col-sm-3 col-lg-3 stats'})
    rightCornerItems = rightCornerDiv.find_all('div', {'class': 'col-12 p-b-i'})

    labelDate = by = fromCountry = maturityStage = looking_for = ''

    for item in rightCornerItems:
        header, content = item.find_all('span')[0].text.lower(), item.find_all('span')[1]
        if header == 'label date':
            labelDate = content.text.strip()
        elif header == 'by':
            by = content.text.strip()
        elif header == 'from':
            fromCountry = content.text.strip()
        elif header == 'maturity stage':
            maturityStage = content.text.strip()
        elif header == 'looking for':
            looking_for = content.text.strip()
    #


    # Middle
    TargetClientItems = soup.find('div', {'class': 'col-12 col-lg-12 p-b-i'}).find_all('li')

    targetClientProfileText = ''
    for item in TargetClientItems:
        targetClientProfileText += item.text + ', '
    targetClientProfileText = targetClientProfileText[:-2]


    TagsItems = soup.find('div', {'class': 'col-12 col-lg-12'}).find_all('li')
    TagsItemsText = ''
    for item in TagsItems:
        TagsItemsText += item.text + ', '
    TagsItemsText = TagsItemsText[:-2]



    sectors = ''

    # First sectors part
    sectorRows = soup.find('div' , {'class' :'sector-rows'}).find_all('div' , {'class' :'sector-row'})
    for sectorRow in sectorRows:
        sectors += sectorRow.text + ', '

    # Second sectors part
    verticalAppTexts = soup.find('div', {'class' : 'columns-steps'})
    applicationListItems = verticalAppTexts.find_all('ul', {'class': 'application-list'})
    for item in applicationListItems :
        sectors += item.text.strip() + ', '
    sectors = sectors[:-2]


    try:
        VideoPlayer = soup.find('div', {'class':'row p-t-i p-b-i'})
        videoUrl = VideoPlayer.find('iframe')['src']
        if 'https://www.youtube.com/embed/' in videoUrl:
            videoUrl = videoUrl.replace('https://www.youtube.com/embed/','https://youtu.be/')

    except:
        videoUrl = ''


    env_benifitsItems = soup.find_all('div', {'class' : 'col-xl-7' })[1].find('ul', {'class':'list'}).find_all('li')
    financial_benifitsItems = soup.find_all('div', {'class' : 'col-xl-7' })[2].find('ul', {'class':'list'}).find_all('li')

    envBenifitText = financialBenifitText = ''

    for item in env_benifitsItems:
        envBenifitText += item.find_all('span')[1].text + ';'

    for item in financial_benifitsItems:
        financialBenifitText += item.find_all('span')[1].text + ';'

    # Activité 
    ActiviteRegionItems = soup.find('div', {'id':'region-list'}).find('div', {'class':'row row-eq-height'}).find_all('div', {'class':'col-sm-6 col-md-4 regions-list'})

    ContinentText = ''
    CountriesText = ''
    for item in ActiviteRegionItems:
        all_ps = item.find_all('p')
        ContinentText += all_ps[0].text + ','

        for a in all_ps[1].find_all('a'):
            CountriesText += a.text + ','

    ContinentText = ContinentText.replace(',,', ',').replace('\n','').strip()[:-1]
    CountriesText = CountriesText.replace(',,', ',').replace('\n','').strip()[:-1]



    RelatedOrgURL = soup.find('div', {'class':'m-b-i-h'}).find('a')['href']


    ComplementarySolutionsItems = soup.find_all('div', {'class' : 'col-xl-12 p-b-i'})[0].find_all('div',{'class':'col-md-3'})

    ComplementarySolutionsText = ''
    for item in ComplementarySolutionsItems:
        title = item.find('p', {'class':'card-title'}).text
        content = item.find('p', {'class':'card-text line-clamp-3'}).text

        a_list = []
        for i in item.find('ul', {'class':'sector-list'}).find_all('li'):
            a_list.append(i.text)

        otherContent = "(" + ",".join(a_list) + ")"
        ComplementarySolutionsText += title + ': ' + content + ' ' + otherContent + ';'

    return [
        index,
        f"https://solarimpulse.com/{solutionUrl}",
        name,
        summary,
        identification,
        labelDate,
        by,
        fromCountry,
        maturityStage,
        looking_for,
        targetClientProfileText,
        TagsItemsText,
        sectors,
        videoUrl,
        envBenifitText,
        financialBenifitText,
        ContinentText,
        CountriesText,
        ComplementarySolutionsText,
        RelatedOrgURL
    ]

df = pd.DataFrame({
    '# dataset' : [],
    'Solution dataset URL' : [],
    'Solution name' : [],
    'Solution on-sentence summary' : [],
    'Identification' : [],
    'Label Date' : [],
    'By' : [],
    'From' : [],
    'Maturity stage' : [],
    'Looking For' : [],
    'Target client profile' : [],
    'Tags' : [],
    'Sectors' : [],
    'Youtube Video URL' : [],
    'The environmental benefits' : [],
    'The Financial benefits' : [],
    'Activity Region - Continent' : [],
    'Activity Region - Countries' : [],
    'Complementary solutions' : [],
    'Organization dataset URL' : [],
})

solutionsDF = pd.read_csv('Scraping Lists pages/SolutionsUrls.csv')
solutionsUrls = solutionsDF['URL']

failed_ones = []
for i in range(1, len(solutionsUrls)+1):
    try:
        solutionURL = solutionsUrls[i-1]
        solutionID = ''
        # getting id from url
        if 'solutions-explorer/' in solutionURL:
            solutionID = solutionURL.replace('solutions-explorer/','')
        whereisQmark = solutionID.find('?')
        solutionID = solutionID[:whereisQmark]
        # logging data
        print('Page ', i, solutionID)
        #getting html file
        with open(f'./downloadSolutionsHTMLS/htmls/{solutionID}.html', 'r', encoding="utf-8") as file:
            html_content = file.read()
        df.loc[i-1] = getDfRow(i, solutionURL, solutionID, html_content)
    except:
        print("FAILLLLLLLLLLLLLLLLLLLLLLLLLL")
        failed_ones.append(solutionID)

df.to_csv('scrapedSolutions.csv', index=False)
print(failed_ones)