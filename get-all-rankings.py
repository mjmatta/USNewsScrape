#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 17:37:19 2022

@author: michaelmatta
"""

import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

browser = webdriver.Chrome('/Users/michaelmatta/Downloads/chromedriver', options=options)

def get_rankings(URL, veteran):
    browser.get(URL)
    time.sleep(2)
    
    no_pagedown = 1
    
    while no_pagedown:
        try:
            button = browser.find_element_by_css_selector("button.button__ButtonStyled-sc-1vhaw8r-1.kaNkh.pager__ButtonStyled-sc-1i8e93j-1.geumwM.type-secondary.size-large")
            button.click()
        except:
            no_pagedown -=1
    
    soup = BeautifulSoup(browser.page_source, 'lxml')
    
    topic = soup.find("h1").text
    
    names = []
    links = []
    locs = []
    ranks = []
    
    for college in soup.find_all("h2", class_="Heading__HeadingStyled-sc-1w5xk2o-0-h2 dEJsBF Heading-sc-1w5xk2o-1 kQuiLM"):
        names.append(college.find("a").text)
        links.append(college.find("a")['href'])
    for loc in soup.find_all("p", class_="Paragraph-sc-1iyax29-0 deEihr"):
        locs.append(loc.text)
    for rank in soup.find_all("p", class_="Paragraph-sc-1iyax29-0 DetailCardOnlineProgramsSearch__RankingParagraph-sc-6mcjcp-5 fEanbm dhMlmy"):
        r = ""
        for part in rank.find_all("span"):
            r += part.text
        ranks.append(r)
    
    print(len(names), len(links), len(locs), len(ranks))
    for i in range(len(names) - len(ranks)):
        ranks.append("Unranked")
        
    df = pd.DataFrame()
    df['Name'] = names
    df['Link'] = links
    df['Location'] = locs
    df['Rank'] = ranks
    
    if veteran:
        df.to_csv('Veterans ' + topic + '.csv', encoding='utf-8', index=False)
    else:
        df.to_csv(topic + '.csv', encoding='utf-8', index=False)
    
page_urls = ['https://www.usnews.com/education/online-education/mba/rankings',
             'https://www.usnews.com/education/online-education/business/rankings',
             'https://www.usnews.com/education/online-education/criminal-justice/rankings',
             'https://www.usnews.com/education/online-education/education/rankings',
             'https://www.usnews.com/education/online-education/engineering/rankings',
             'https://www.usnews.com/education/online-education/computer-information-technology/rankings',
             'https://www.usnews.com/education/online-education/nursing/rankings']

vet_urls = ['https://www.usnews.com/education/online-education/mba/veteran-rankings',
             'https://www.usnews.com/education/online-education/business/veteran-rankings',
             'https://www.usnews.com/education/online-education/criminal-justice/veteran-rankings',
             'https://www.usnews.com/education/online-education/education/veteran-rankings',
             'https://www.usnews.com/education/online-education/engineering/veteran-rankings',
             'https://www.usnews.com/education/online-education/computer-information-technology/veteran-rankings',
             'https://www.usnews.com/education/online-education/nursing/veteran-rankings']

start = int(round(time.time()))

for url in page_urls:
    start_time = int(round(time.time()))
    get_rankings(url, 0)
    end_time = int(round(time.time()))
    print("Elapsed: " + str(end_time - start_time) + " Seconds for: " + url)
    
for url in vet_urls:
    start_time = int(round(time.time()))
    get_rankings(url, 1)
    end_time = int(round(time.time()))
    print("Elapsed: " + str(end_time - start_time) + " Seconds for: " + url)
    
end = int(round(time.time()))

print("Total time: " + str(end-start) + " seconds.")