'''
Web scrapper

@author: Guillermo Quintana Pelayo
@date: 28-05-2020
'''
import requests
import pandas as pd
import os
import json
from bs4 import BeautifulSoup

# Get the data page directly from the webserver
url = 'https://api.ycombinator.com/companies/export.json?callback=true'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}
# Obtain page as html
page = requests.get(url,timeout=(3.05, 27),headers=headers)
# Transform html to a readableformat
soup = BeautifulSoup(page.content, 'html.parser')
# Parse text to remove unwanted formatting
text = soup.text
text = text.replace('setupCompanies(','')
text = text.replace(');','')
# Load data as json format
companies = json.loads(text)

# Create dataframe and save it into an xlsx
l = []
for c in companies:
    row = [c['name'],c['url'],c['batch'],c['vertical'],c['description'],str(c['dead'])]
    l.append(row)

df = pd.DataFrame(l, columns=['Name','URL','Batch','Vertical','Description','Dead'])
df.to_excel('../out/parsed_data.xlsx')
