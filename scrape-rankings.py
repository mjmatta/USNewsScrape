#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 19:30:47 2022

@author: michaelmatta
"""

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

browser = webdriver.Chrome('/Users/michaelmatta/Downloads/chromedriver', options=options)   

URL = 'https://www.usnews.com/education/online-education/criminal-justice/rankings'

browser.get(URL)
time.sleep(2)

elem = browser.find_element_by_tag_name("body")

no_pagedown = 40

while no_pagedown:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_pagedown -= 1
    
print("done scrolling")
    
post_elems = browser.find_elements_by_class_name("Paragraph-sc-1iyax29-0 deEihr")

soup = BeautifulSoup(browser.page_source, 'lxml')

names = []
links = []
locs = []
ranks = []

for college in soup.find_all("h2", class_="Heading__HeadingStyled-sc-1w5xk2o-0-h2 dEJsBF Heading-sc-1w5xk2o-1 kQuiLM"):
        names.append("University Name: " + college.find("a").text + "\n")
        links.append("University Link: " + college.find("a")['href'] + "\n")
for loc in soup.find_all("p", class_="Paragraph-sc-1iyax29-0 deEihr"):
    locs.append("University Location: " + loc.text + "\n")
for rank in soup.find_all("p", class_="Paragraph-sc-1iyax29-0 DetailCardOnlineProgramsSearch__RankingParagraph-sc-6mcjcp-5 fEanbm dhMlmy"):
    r = ""
    for part in rank.find_all("span"):
        r += part.text
    ranks.append("University Rank:" + r + "\n")

print(len(names), len(links), len(locs), len(ranks))

with open('criminal-justice-rankings.txt', 'w') as f:
    for i in range(len(names)):
        f.write(names[i] + links[i] + locs[i])
        try:
            f.write(ranks[i])
        except IndexError:
            f.write("University Rank: Unranked\n")
        f.write("\n")