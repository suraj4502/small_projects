import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}



# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_discription(soup):
    try:
        # Find the <div> tag with id="featurebullets_feature_div"
        div_tag = soup.find('div', id='featurebullets_feature_div')

        # Find all <span> tags with class="a-list-item" within the <div> tag
        span_tags = div_tag.find_all('span', class_='a-list-item')

        # Extract the text from each <span> tag
        text_list = [span_tag.get_text(strip=True) for span_tag in span_tags]

    except AttributeError:
        text_list = ""
        
    return text_list


def get_details(soup):
    try:
        # Find the <div> tag with id="featurebullets_feature_div"
        div_tag = soup.find('div',id="detailBulletsWrapper_feature_div")

        # Find all <span> tags with class="a-list-item" within the <div> tag
        span_tags = div_tag.find_all('span', class_='a-list-item')

        # Extract the text from each <span> tag
        text_list = [span_tag.get_text(strip=True) for span_tag in span_tags]

    except AttributeError:
        text_list = ""
        
    return text_list


def get_price(soup):
    try:
        
        price = soup.find('span',class_ ='a-offscreen').text.strip()
    except AttributeError:
        price =""

    return price
    
    
 



def get_product_links(url):
    
    # first lets get the links of all the products on the page
    
    # sending a http request
    webpage = requests.get(url, headers=HEADERS)
    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    # Store the links
    links_list = []
    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))  
        #here we have all the links
            
            
    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    info = {"title":[], "discription":[], "details":[], "price":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        if "https://www.amazon.com/" in link:
            new_webpage = requests.get( link, headers=HEADERS)
        else:
            new_webpage = requests.get("https://www.amazon.com/" + link, headers=HEADERS)
        print("https://www.amazon.com" + link)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        info['title'].append(get_title(new_soup))
        info['discription'].append(get_discription(new_soup))
        info['details'].append(get_details(new_soup))
        info['price'].append(get_price(new_soup))
    
    return info
    
        
            


    
 # The webpage URL
URL = "https://www.amazon.com/s?k=clothing&crid=2XF89HOMSFDER&sprefix=clothing%2Caps%2C289&ref=nb_sb_noss_2"


list_1 = get_product_links(url=URL)
print(list_1)

























