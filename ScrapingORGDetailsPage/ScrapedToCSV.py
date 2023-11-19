import httpx, re
from bs4 import BeautifulSoup
import pandas as pd

def getImageURLfromStyle(text):
    url_pattern = r'background-image:url\((.*?)\)'
    match = re.search(url_pattern, text)
    if match:
        url = match.group(1)

        # testing if ' in first and ' in last
        if len(url) > 0 and url[0] == url[-1] == "'":
            return url[1:-1]
        else:
            return url
    else:
        return ''


def getDfRow(index, organizationUrl, organizationID, html_content):
    # Parse the HTML into a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    name = soup.find('h1', {'class': 'title title-h1 left-marker reveal-block'}).text.replace('Member - ', '')

    logo_styleCODE = soup.find('div', {'class':'logo'})['style']
    logo = getImageURLfromStyle(logo_styleCODE)
    shortDesc = soup.find('p', {'class':'title title-h5 reveal-block p-r-i'}).text
    about = soup.find('div', {'class':'col-lg-6 col-xl-4 offset-lg-1 offset-xl-1 p-t-xs-section p-b-xl-section'}).find('div').text
    try:
        website = soup.find('a', {'class':'btn-animated-border animated-next reveal-block'})['href']
    except:
        website = ''
        print('No website')
    number_of_solutions = len(soup.find_all('a', {'class':'card card-solutions reveal-block'}))

    # SDG APPLICATION DIV
    sdgAPPDiv = soup.find('div', {'class': "sdg-aplication-section"})

    sdgContentContainer = sdgAPPDiv.find('div', {'class' : 'col-sm-7'})
    activeContentItems = sdgContentContainer.find_all('div', {'class' : 'inner-box active'})
    finalSDGtext = ''
    for item in activeContentItems:
        finalSDGtext += item.find('div', {'class':'title'}).text + ' - ' + item.find('div', {'class':'text'}).text +', '
    finalSDGtext = finalSDGtext[:-2] # Removing the last ', ' 
    try:
        sdgDocumentContainer =  sdgAPPDiv.find('div', {'class':'col-sm-4 offset-sm-1'})
        urlDocument = sdgDocumentContainer.find('a', {'class':'btn-animated-border animated-next'})['href']
    except:
        urlDocument = ''
        print('No urlDocument')

    # stats Content
    statsDiv = soup.find('div', {'class':'row p-b-section'})
    statItems = statsDiv.find_all('div', {'class': 'col-sm-4'})

    companytype = founded = companysize = membertype = founder1Name = founder1LastName = founder2Name = founder2LastName= founder3Name = founder3LastName = headquarters = facebook = twitter = linkedin = ''

    for item in statItems:
        header, content = item.find_all('span')[0].text.lower(), item.find_all('span')[1]
        if header == 'type':
            companytype = content.text

        elif header == 'founded':
            founded = content.text

        elif header == 'company size':
            companysize = content.text

        elif header == 'member type':
            for type in content.find_all('div', {'class':'tag'}):
                membertype += type.text + ', '
            membertype = membertype[:-2]

        elif header == 'founders':
            if content.text != '':
                if ',' in content.text:
                    founders = content.text.split(',')
                    for i in range(len(founders)):
                        try:
                            firstName, lastName = founders[i].strip().split(' ')[0], founders[i].strip().split(' ')[1]
                            if i == 0:
                                founder1Name, founder1LastName = firstName, lastName
                            elif i== 1:
                                founder2Name, founder2LastName = firstName, lastName
                            elif i== 2:
                                founder3Name, founder3LastName = firstName, lastName
                        except:
                            print('NO FOUNDERS OK')
                            pass
                else:
                    this_one_founder_words = content.text.split(' ')
                    if len(this_one_founder_words) == 2:
                        founder1Name, founder1LastName = this_one_founder_words[0], this_one_founder_words[1]
                    else:
                        founder1Name, founder1LastName = this_one_founder_words[0], " ".join(this_one_founder_words[1:])

        elif header == 'headquarters':
            count_of_commas = content.text.count(',')
            if ',' in content.text and count_of_commas == 1:
                headquarters = content.text.split(',')[1]
            else:
                headquarters = content.text

        elif header == 'social network':
            for aTag in content.find_all('a'):
                if 'twitter' in aTag['href']:
                    twitter = aTag['href']
                elif 'linkedin' in aTag['href']:
                    linkedin = aTag['href']
                elif 'facebook' in aTag['href']:
                    facebook = aTag['href']

    '''
    print(name, logo, shortDesc, about, website, finalSDGtext, urlDocument)
    print("Company Type:", companytype)
    print("Founded:", founded)
    print("Company Size:", companysize)
    print("Member Type:", membertype)
    print("Founder 1:", founder1Name, founder1LastName)
    print("Founder 2:", founder2Name, founder2LastName)
    print("Founder 3:", founder3Name, founder3LastName)
    print("Headquarters:", headquarters)
    print("Facebook:", facebook)
    print("Twitter:", twitter)
    print("LinkedIn:", linkedin)
    print("Number of solutions", number_of_solutions)
    '''
    return [
        index,
        f"https://solarimpulse.com{organizationUrl}",
        name,
        logo,
        shortDesc,
        companytype,
        founded,
        companysize,
        membertype,
        founder1Name,
        founder1LastName,
        founder2Name,
        founder2LastName,
        founder3Name,
        founder3LastName,
        headquarters,
        facebook,
        twitter,
        linkedin,
        urlDocument,
        about,
        website,
        finalSDGtext,
        number_of_solutions
    ]





df = pd.DataFrame({
    '# dataset' : [],
    'Organization dataset URL' : [],
    'Organization name' : [],
    'Logo' : [],
    'Organization short description' : [],
    'Organization type' : [],
    'Founded' : [],
    'Company size' : [],
    'Member type' : [],
    'Founder 1 - First name' : [],
    'Founder 1 - Last name' : [],
    'Founder 2 - First name' : [],
    'Founder 2 - Last name' : [],
    'Founder 3 - First name' : [],
    'Founder 3 - Last name' : [],
    'Headquarters' : [],
    'Facebook profile link' : [],
    'Twitter profile link' : [],
    'LinkedIN profile link' : [],
    'Documents' : [],
    'About' : [],
    'Website link' : [],
    'SDG’s of application' : [],
    'Number of solutions' : [],
})


organizationsDF = pd.read_csv('Scraping Lists pages/AllianceUrls.csv')
organizationsUrls = organizationsDF['URL']

failed_ones = []
for i in range(1, len(organizationsUrls)+1):
    #try:
    organizationURL = organizationsUrls[i-1]
    organizationID = ''
    # getting id from url
    if '/companies/' in organizationURL:
        organizationID = organizationURL.replace('/companies/','')
    # logging data
    print('Page ', i, organizationID)
    #getting html file
    with open(f'./downloadOrgHTMLS/htmls/{organizationID}.html', 'r', encoding="utf-8") as file:
        html_content = file.read()
    df.loc[i-1] = getDfRow(i, organizationURL, organizationID, html_content)
    """
    except:
        print("FAILLLLLLLLLLLLLLLLLLLLLLLLLL")
        failed_ones.append(organizationID)"""

df.to_csv('scrapedOrganizations.csv', index=False)
print(failed_ones)