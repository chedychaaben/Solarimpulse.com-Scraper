import pandas as pd

orgDF = pd.read_csv('scrapedOrganizationsOK.csv')
solutionDF = pd.read_csv('scrapedSolutionsOK.csv')


# Create an empty DataFrame
columns = ['# dataset', 'Solution dataset URL', 'Solution name', 'Solution on-sentence summary',
           'Identification', 'Label Date', 'By', 'From', 'Maturity stage', 'Looking For',
           'Target client profile', 'Tags', 'Sectors', 'Youtube Video URL', 'The environmental benefits',
           'The Financial benefits', 'Activity Region - Continent', 'Activity Region - Countries',
           'Complementary solutions', 'Organization dataset URL', 'Organization name', 'Logo',
           'Organization short description', 'Organization type', 'Founded',
           'Company size', 'Member type', 'Founder 1 - First name', 'Founder 1 - Last name',
           'Founder 2 - First name', 'Founder 2 - Last name', 'Founder 3 - First name',
           'Founder 3 - Last name', 'Headquarters', 'Facebook profile link', 'Twitter profile link',
           'LinkedIN profile link', 'Documents', 'About', 'Website link', 'SDG’s of application',
           'Number of solutions']

# Create an empty DataFrame with the given column names
newSolutionDF = pd.DataFrame(columns=columns)

print(newSolutionDF)


counter = 0
for i,solutionrow in solutionDF.iterrows():
    orgURL = solutionrow['Organization dataset URL']
    if '/companies/view/' in orgURL:
        orgIDofSolutions = orgURL.replace('/companies/view/', '')
    else:
        orgIDofSolutions = ''

    # Mergin with ORDID
    try:
        matched_row_with_ORGID = orgDF[orgDF['Organization dataset URL'] == f'https://solarimpulse.com/companies/{orgIDofSolutions}'].iloc[0]
    except:
        matched_row_with_ORGID = pd.Series("", index=orgDF.columns)

    # Creating ...
    newSolutionDF.loc[counter] = [
        solutionrow['# dataset'],
        solutionrow['Solution dataset URL'],
        solutionrow['Solution name'],
        solutionrow['Solution on-sentence summary'],
        solutionrow['Identification'],
        solutionrow['Label Date'],
        solutionrow['By'],
        solutionrow['From'],
        solutionrow['Maturity stage'],
        solutionrow['Looking For'],
        solutionrow['Target client profile'],
        solutionrow['Tags'],
        solutionrow['Sectors'],
        solutionrow['Youtube Video URL'],
        solutionrow['The environmental benefits'],
        solutionrow['The Financial benefits'],
        solutionrow['Activity Region - Continent'],
        solutionrow['Activity Region - Countries'],
        solutionrow['Complementary solutions'],

        
        matched_row_with_ORGID['Organization dataset URL'],
        matched_row_with_ORGID['Organization name'],
        matched_row_with_ORGID['Logo'],
        matched_row_with_ORGID['Organization short description'],
        matched_row_with_ORGID['Organization type'],
        matched_row_with_ORGID['Founded'],
        matched_row_with_ORGID['Company size'],
        matched_row_with_ORGID['Member type'],
        matched_row_with_ORGID['Founder 1 - First name'],
        matched_row_with_ORGID['Founder 1 - Last name'],
        matched_row_with_ORGID['Founder 2 - First name'],
        matched_row_with_ORGID['Founder 2 - Last name'],
        matched_row_with_ORGID['Founder 3 - First name'],
        matched_row_with_ORGID['Founder 3 - Last name'],
        matched_row_with_ORGID['Headquarters'],
        matched_row_with_ORGID['Facebook profile link'],
        matched_row_with_ORGID['Twitter profile link'],
        matched_row_with_ORGID['LinkedIN profile link'],
        matched_row_with_ORGID['Documents'],
        matched_row_with_ORGID['About'],
        matched_row_with_ORGID['Website link'],
        matched_row_with_ORGID['SDG’s of application'],
        matched_row_with_ORGID['Number of solutions']

    ]

    counter += 1

newSolutionDF.to_csv('newSolutionDF.csv', index=False)