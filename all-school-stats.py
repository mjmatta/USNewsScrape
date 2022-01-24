#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 14:49:03 2022

@author: michaelmatta
"""

import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
import os

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")

#TODO: CHANGE CHROMEDRIVER PATH HERE
browser = webdriver.Chrome('/Users/michaelmatta/Downloads/chromedriver', options=options)   

def get_stats_for_program(program):
    df = pd.read_csv(program + '.csv', encoding='utf-8')
    links = df['Link']
    for url in links:
        browser.get(url)
        time.sleep(2)
        elem = browser.find_element_by_tag_name("body")
    
        buttons = browser.find_elements_by_css_selector('.Bellow__HeadingButton-sc-1wt7bw1-1.cTMQPc')
        buttons.append(browser.find_element_by_css_selector('.Bellow__HeadingButton-sc-1wt7bw1-1.ifMnd'))
        #print(len(buttons))
        #buttons.insert(2, browser.find_element_by_xpath('#chevron'))
        
        for b in buttons:
            i = 1
            while i:
                try:
                    b.click()
                    i -= 1
                except ElementClickInterceptedException:
                    elem.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.2)
            time.sleep(0.5)
            
        
            
        soup = BeautifulSoup(browser.page_source, 'lxml')
        
        name = soup.find("h1").text
        
        text = "Best Online Programs Ranking Indicators\n\n"
        
        ind_labels = soup.find_all("p", class_="Indicators__Label-sc-18u90m1-2 dQREVe t4")
        ind_vals = soup.find_all("p", class_="Indicators__Value-sc-18u90m1-1 ggkQDP t4")
        for i in range(len(ind_labels)):
            text += (ind_labels[i].text + ": " + ind_vals[i].text + "\n")
            
        sections = soup.find_all("div", class_="Bellow__BellowWrapper-sc-1wt7bw1-0")
        
        labels = ["Applying", "Academics", "Student Body", "Technology & Support", "Paying for School"]
        
        for i in range(len(sections)):
            text += ("\n" + labels[i] + "\n\n")
            divs = sections[i].find_all("div", class_="Box-w0dun1-0")
            for div in divs:
                ps = div.find_all("p")
                try:
                    text += (ps[0].text + ": " + ps[1].text + "\n")
                except:
                    #print("Failed for: " + div.text +  "\n\n" + str(div) + "\n\n\n")
                    pass
                    
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, program)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        with open((program + '/' + name + '.txt'), 'w') as f:
            f.write(text)


progs = ["Best Online MBA Programs", "Best Online Master's in Business Programs",
         "Best Online Master's in Criminal Justice Programs", "Best Online Master's in Education Programs",
         "Best Online Master's in Engineering Programs", "Best Online Master's in Information Technology Programs",
         "Best Online Master's in Nursing Programs", "Veterans Best Online Master's in Business Programs",
         "Veterans Best Online Master's in Criminal Justice Programs", "Veterans Best Online Master's in Education Programs",
         "Veterans Best Online Master's in Engineering Programs", "Veterans Best Online Master's in Information Technology Programs",
         "Veterans Best Online Master's in Nursing Programs", "Veterans Best Online MBA Programs"]

start = int(round(time.time()))

for prog in progs:
    start_time = int(round(time.time()))
    get_stats_for_program(prog)
    end_time = int(round(time.time()))
    print("Elapsed: " + str(end_time - start_time) + " Seconds for: " + prog)
    
end = int(round(time.time()))

print("Total time: " + str(end-start) + " seconds.")