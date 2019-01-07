import requests
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver

# TODO: Get url from the user
# TODO: Validate url

# Get data 
# url = 'https://www.tori.fi/varsinais-suomi/Galaksikuvioitu_lapparilaukku_13__49934820.htm?ma=1'
# url = 'https://www.tori.fi/keski-pohjanmaa/Vanhempi_minulle_harrasteautoksi_1960___1979_51308487.htm?ca=18&w=3'
# url = 'https://www.tori.fi/varsinais-suomi/Kookas_koristeellinen_viskilasi_52516168.htm?ma=1'
url = 'https://www.tori.fi/etela-pohjanmaa/Koivupoyta__katajaisella_reunuslistalla__52426209.htm?ca=18&w=3'
data = requests.get(url)

# Load the page into beautiful soup
soup = BeautifulSoup(data.text, 'html.parser')

# --- Title ---
# div = topic, inside h1
# strip() removes the leading and the trailing whitespace, internal spaces are preserved
#title = soup.find('div', {'class' : 'topic'}).find('h1').text.strip();
title = soup.find('h1', {'itemprop' : 'name'}).text.strip()
print(title)

# --- Price ---
# Extract the numbers from the result (gets rid off euro symbols) and turn them into a number array
priceinfo = soup.find('span', {'itemprop' : 'price'}).text
prices = [int(s) for s in re.findall(r'\d+', priceinfo) if s.isdigit()]

# Select the smaller price (if there's been a price change and multiple prices are displayed)
price = min(prices)
print(price)

# --- Description ---
description = soup.find('div', {'itemprop' : 'description'}).text.strip()
description = description.strip('Lisätiedot')
description = description.replace('\t', '')
description = description.replace('\n', '')
#re.sub(r'([ \t]+)', '-', description)
print(description)

'''
Items we'll get will be
1. 'Etusivu' (useless, we can scrap this)
2. Maakunta
3. Category
4. Subcategory (not always present)
'''
categorydata = []
for info in soup.find_all('div', {'itemtype' : 'http://data-vocabulary.org/Breadcrumb'}):
	for span in info.find_all('span', {'itemprop' : 'title'}):
			categorydata.append(span.text.strip())

print(categorydata)

area = categorydata[1]
category = categorydata[2]
if(len(categorydata) == 4): # Subcategory is not always present
	subcategory = categorydata[3]

print("Maakunta: ", area)
print("Kategoria: ", category)
if subcategory:
	print(subcategory)

# Only works for Myydään (selling) -postings
adtype = soup.find('tr', {'itemprop' : 'offers'}).find('td', {'class' : 'value'}).text
print(adtype)

# --- City ---
citydata = soup.find("meta",  property="og:title")
print(citydata)
city = re.search('\,\s(.*)" property', str(citydata)).group(1)
print(city)

# --- Location (zip code) ---

zippattern = re.compile(r'tori\.banner\.feedObj\["zipcode"\] = "(.*)";')
zipdata = soup.find("script", text=zippattern)
zipcode = zippattern.search(zipdata.text).group(1)
print('Zipcode: ', zipcode)

# NEED
# - Photos
# - Ad type


# SELENIUM
'''
browser = webdriver.Chrome('/Applications/chromedriver')
#browser.get('https://www2.tori.fi')
#elem = browser.find_element_by_link_text('Jätä ilmoitus')
#print(elem.text)
#print(elem.get_attribute('href'))
#elem.click()
browser.get('https://www2.tori.fi/ai/form/0?ca=18')

titleField = browser.find_element_by_id('subject')
titleField.send_keys(title)

dscrField = browser.find_element_by_id('body')
dscrField.send_keys(description)
'''

# select = Select(driver.find_element_by_id('fruits01'))
# select.select_by_visible_text('')

