from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
from selenium.webdriver.chrome.options import Options

URL = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=iphone&_sacat=0"

service = Service(executable_path="C:\Development\chromedriver.exe")
options = Options()
options.add_argument('--incognito')
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

result = []
header_contents = soup.find_all('li', class_='s-item s-item__pl-on-bottom')

for content in header_contents:
    title = content.find('div', class_="s-item__title").text
    try:
        price = content.find('span', class_="s-item__price").text
    except:
        continue
    try:
        location = content.find('span', class_="s-item__location s-item__itemLocation").text
    except:
        continue
    try:
        review = content.find('span', class_="s-item__reviews-count").text
    except:
        review = "no review"
    final_data = {
        'title': title,
        'price': price,
        'location': location,
        'review': review,
    }
    result.append(final_data)

# writing json
with open('json_result.json', 'w') as outfile:
    json.dump(result, outfile)
    # read json
with open('json_result.json') as json_file:
    final_data = json.load(json_file)

    df = pd.DataFrame(final_data)
    df.to_csv('result.csv', index=False)
    df.to_excel('result.xlsx', index=False)