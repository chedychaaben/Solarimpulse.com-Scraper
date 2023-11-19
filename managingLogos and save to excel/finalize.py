import pandas as pd
import requests

orgDF = pd.read_csv('scrapedOrganizationsOK.csv')
solutionDF = pd.read_csv('newSolutionDFOK.csv')

def download_image(index, url, code):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Generate the file name using the index
        file_name = f"images/{index}_{code}.png"
        
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Image {index} downloaded successfully.")
        if 'images/' in file_name:
            file_name = file_name.replace('images/', '')
        
        if '.png' in file_name:
            file_name = file_name.replace('.png', '')

        return file_name
    
    except requests.HTTPError:
        print(f"Failed to download image {index} from URL: {url}")
        return ''
    
    except Exception as e:
        print(f"An error occurred while downloading image {index}: {str(e)}")
        return ''

def download_pdf(index, url, code):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Generate the file name using the index
        file_name = f"documents/{index}_{code}.pdf"
        
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Document {index} downloaded successfully.")

        if 'documents/' in file_name:
            file_name = file_name.replace('documents/', '')

        
        if '.pdf' in file_name:
            file_name = file_name.replace('.pdf', '')
        
        return file_name
    
    except requests.HTTPError:
        print(f"Failed to download document {index} from URL: {url}")
        return ''
    except Exception as e:
        print(f"An error occurred while downloading document {index}: {str(e)}")
        return ''


def download_image(index, url, code):
    try:
        with open(f"images/{index}_{code}.png", 'r') as f:
            pass
        return f"{index}_{code}"
    except:
        return ''

def download_pdf(index, url, code):
    try:
        with open(f"documents/{index}_{code}.pdf", 'r') as f:
            pass
        return f"{index}_{code}"
    except:
        return ''


for i,solutionrow in solutionDF.iterrows():
    this_logo_url = solutionrow['Logo']
    new_logo_name = download_image(i+1, this_logo_url, 'C')

    
    this_document_url = solutionrow['Documents']
    new_document_name = download_pdf(i+1, this_document_url, 'P')

    # Saving new values
    solutionDF.at[i, 'Logo'] = new_logo_name
    solutionDF.at[i, 'Documents'] = new_document_name
    print(new_logo_name ,new_document_name)


for i,orgrow in orgDF.iterrows():
    this_logo_url = orgrow['Logo']
    new_logo_name = download_image(i+1, this_logo_url, 'L')

    
    this_document_url = orgrow['Documents']
    new_document_name = download_pdf(i+1, this_document_url, 'B')

    # Saving new values
    orgDF.at[i, 'Logo'] = new_logo_name
    orgDF.at[i, 'Documents'] = new_document_name

    print(new_logo_name ,new_document_name)

import numpy as np
# Copmany size float to int for both 
solutionDF['Company size'] = solutionDF['Company size'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)
orgDF['Company size'] = orgDF['Company size'].replace([np.inf, -np.inf], np.nan).fillna(0).astype(int)

solutionDF.to_csv('SolutionsAfterDownloading.csv', index=False)
orgDF.to_csv('OrganizationsAfterDownloading.csv', index=False)