#importing libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Getting the request and making Beatuiful soup object
url = "https://www.makaan.com/bangalore-residential-property/rent-property-in-bangalore-city"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Getting the number of pages in the website
num_of_pages = soup.find('li', class_ = "dots").next_sibling.text
data = []

# Getting beautiful soup object and data of every page
for page_num in range(1,int(num_of_pages)):
    page_url = "https://www.makaan.com/bangalore-residential-property/rent-property-in-bangalore-city?page="+str(page_num)
    page_req = requests.get(page_url)
    page_soup = BeautifulSoup(page_req.content, 'html.parser')
    
    sections = page_soup.find_all('div', attrs = {"class":"cardLayout clearfix", "data-type":"listing-card"})

    for section in sections:
        bhk = section.find('span',class_ = "val")
        bhkstring = bhk.text + bhk.next_sibling.text
        type = bhk.next_sibling.next_sibling.text
        locality = section.find('span',attrs = {"itemprop":"addressLocality"}).text
        region = section.find('span',attrs = {"itemprop":"addressRegion"}).text
        price = section.find('span',attrs = {"class":"val","itemprop":"offers"}).text + " Rs"
        area = section.find('td',class_ = "size").text + "sq ft"
        status = section.find('tr', class_ = "hcol w44").text
        # Checking if the deposit_tag object is a None type object or not
        deposit_tag = section.find('li', class_ = "keypoint", title = "deposit")
        if(deposit_tag): # Not None type
            deposit = deposit_tag.text
        else:            # None type
            deposit = "Null"  

        # Checking if the beautiful_tag object is a None type object or not
        bathrooms_tag = section.find('li', class_ = "keypoint", title = "bathrooms")
        if(bathrooms_tag): # Not None type
            bathrooms = bathrooms_tag.text
        else:              # None type
            bathrooms = "None"

        # Checking if the description_tag object is a None type object or not
        description_tag = section.find('div',class_ = "listing-description")
        if(description_tag): # Not None type
            description = description_tag.div.text
        else:                # None type
            description = "Null"

        link = section.find('a',class_ = "typelink")['href']

        info = [bhkstring,type,locality,region,price,area, status,deposit,bathrooms,description,link]
        data.append(info)  # Adding all the info in the data 


header = ['BHK','Type','Locality','Region','Price','Area','Status','Deposit','Bathrooms','Description','Link']
df = pd.DataFrame(data,columns=header) # Converting to dataframe
df.to_csv('housing.csv') # Creating csv file