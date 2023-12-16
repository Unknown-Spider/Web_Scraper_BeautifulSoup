import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv  
import re  #Ragular Expression 
import requests 

                #Product Scraper
data  = {'title': [], 'price': []}
relink = {'relink': []}

url = " https://www.amazon.in/s?k=iphone&ref=nb_sb_noss_1"
url1 = " https://vegamovies.boo/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url,headers=headers)  
r1 = requests.get(url1,headers=headers)  

soup = BeautifulSoup(r.text, 'html.parser')

spans = soup.select("span.a-size-medium.a-color-base.a-text-normal")


prices = soup.select("span.a-price")
for span in spans:
        print(span.string)
        data["title"].append(span.string)

for price in prices:
        if not("a-text-price" in price.get("class")):
            print(price.find("span").get_text())
            data["price"].append(price.find("span").get_text())

            if len(data["price"]) == len(data["title"]):
                   break

df = pd.DataFrame.from_dict(data)
df.to_csv("data.csv", index = False)



                        # Link Extractor

soup = BeautifulSoup(r1.content, 'html.parser')

# find all links on the page

links = soup.find_all('a', href=True)

# print the href attribute of each link
for link in links:
    # print(link.get('href'))
    relink["relink"].append(link.get('href'))
df = pd.DataFrame.from_dict(relink)
df.to_csv("url.csv", index = False)


                        # Number Extractor
 
phone_regex = re.compile(r'''(
                        (\d{3}|\(\d{3}\))?
                        (\s|-|\.)?
                        (\d{3})
                        (\s|-|\.)
                        (\d{4})
                        (\s*(ext|x|ext.)\s*(\d{2,5}))?)''', re.VERBOSE)


                        # Mail Extractor
   
# mail id expression code
email_regex = re.compile(r'''(
                        [a-zA-Z0-9._%+-]+
                        @
                        [a-zA-Z0-9.-]+
                         .
                        [a-zA-Z.]+
                        (\.[a-zA-Z.]{0,8}))''', re.VERBOSE)
# mail id expression code
email_regex = re.compile(r'''(
                        [a-zA-Z0-9._%+-]+
                        @
                        # [a-zA-Z0-9._+-gmail]+
                        #  .
                        [a-zA-Z.]+
                        (\.[a-zA-Z.]{0,8}))''', re.VERBOSE)
 
# Main fetch data code 
with open("website_urls.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')    
     
    for row in csv_reader:
        page_url = row[0]        
        print("Opening URL:", page_url)
        page_data = requests.get(page_url)
 
        
        page_html = str(page_data.content)        
         
        matches = []
        for groups in phone_regex.findall(page_html):
            phone_numbers = '-'.join([groups[1], groups[3], groups[5]])
            if groups[8] != '':
                phone_numbers += ' x' + groups[8]            
            matches.append(phone_numbers)
 
        for groups in email_regex.findall(page_html):
            matches.append(groups[0])

        
         
        print('\n'.join(matches))

