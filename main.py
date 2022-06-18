from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://www.makaan.com/bangalore-residential-property/rent-property-in-bangalore-city"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')


num_of_pages = soup.find('li', class_ = "dots").next_sibling.text
data = []

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

        deposit_tag = section.find('li', class_ = "keypoint", title = "deposit")
        if(deposit_tag):
            deposit = deposit_tag.text
        else:
            deposit = "Null"  

        bathrooms_tag = section.find('li', class_ = "keypoint", title = "bathrooms")
        if(bathrooms_tag):
            bathrooms = bathrooms_tag.text
        else:    
            bathrooms = "None"

        description_tag = section.find('div',class_ = "listing-description")
        if(description_tag):
            description = description_tag.div.text
        else:
            description = "Null"

        link = section.find('a',class_ = "typelink")['href']

        info = [bhkstring,type,locality,region,price,area, status,deposit,bathrooms,description,link]
        data.append(info)   


header = ['BHK','Type','Locality','Region','Price','Area','Status','Deposit','Bathrooms','Description','Link']
df = pd.DataFrame(data,columns=header)
df.to_csv('housing.csv')