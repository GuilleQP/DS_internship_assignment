# Data Science Internship Assignment
![](https://img.shields.io/badge/made_with-Python_3.6-red?style=flat-square) ![](https://img.shields.io/badge/docs-Markdown-lightblue?style=flat-square)

## Tasks
### Classification
- Classify the companies **easily**. Fill in the correct type in column K ("TYPE").
- In the tab "Count" fill in the number of entities per type.
- Build a list of keywords.

### Scraping
- Retrieve data from https://www.ycombinator.com/companies/

## Instructions

Install requirements for Python 3.6+
    
    pip install -r requirements.txt

To execute the classifier run (inside src):

    python classify.py

To execute the web scraper run (inside src):

    python scrap.py

It can take a few seconds and the results are then inside out/.

## Description

For the data classification I opted for a greedy approach that counts the number of occurrences inside a keywords list. This list was implemented into a json format so that it is easy to modify and customize. I think an unsupervised learning approach is an overkill for this data size but it would be a good option if the data increases in size and also in class types. It is coded in a class format instead of a simple sequential script since this type of classifier surely needs more methods in the future.

For the web scraper I used requests and BeautufulSoup, I personally prefer to directly use wget but I used those instead because I don't know if this code is going to run on a linux or a windows machine and also the website doesn't require a login or any form request. The website provided needs to wait for a js to load the data so I directly obtained the data from the route that this js is calling inside the webserver, it's simpler than waiting for the js to load and then remove all the unwanted text inside the html.

All the results are combined in Data_Science_Assignment_results.xlsx.

Made by Guillermo Quintana Pelayo