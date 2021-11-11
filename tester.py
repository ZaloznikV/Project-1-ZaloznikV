# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
from selenium.webdriver.common.by import By
print(19)
PATH = r"chromedriver.exe"
file = open('article_urls.txt', 'r')
Lines = file.readlines()

# for line in Lines:
#     print(line)
#     time.sleep(1)
#prvega je potrebno ignorirati ker ni novica ampak podstran
site_url = "https://www.rtvslo.si/slovenija/skupaj-naprej-v-premagovanje-epidemije/600811"


options = webdriver.ChromeOptions()
options.add_argument('window-size=2880,1800')
options.add_argument("--start-maximized") #so I can see it in fullscreen on laptop
driver = webdriver.Chrome(PATH, options=options)
driver.get(site_url)

print("Starting to get data from article: ",driver.title)


author_class = driver.find_element_by_class_name("author") 
author_name = author_class.find_element_by_class_name("author-name")
authors = author_name.text
print("Authors are: ", authors)
time.sleep(1)

authors = list(authors.split(", "))

title_class = driver.find_element_by_class_name("article-header")
title = title_class.find_element_by_tag_name("h1").text
print("Title is: ", title)
time.sleep(1)

date_class = driver.find_element_by_class_name("publish-meta")
print("#########################")
date_all = list((date_class.text).split("\n")) 

print(  date_all )
change = "NO"
if len(date_all) > 1:
    if "Zadnji poseg:" in date_all[1]:
        change = "YES"
        

date_full = list((date_class.text).split("\n"))[0]
date, hour = list(date_full.split("ob"))
print("Article was published on {}, at {}.".format(date, hour))
time.sleep(1)

print("Since publishing article was changed later: {}.".format(change))
time.sleep(1)


article_tags_class = driver.find_element_by_class_name("article-tags")
articles_tags = article_tags_class.find_elements_by_class_name("tag")

article_tags = []

for article_tag in articles_tags:
    article_tags.append(article_tag.text)
print("Article tags are: ", article_tags)
time.sleep(1)
    
section_class = driver.find_element_by_class_name("section-title")
section_tag_a = section_class.find_element_by_tag_name('a')
section_tag = section_tag_a.get_attribute('aria-label')
print("Section tag is: ", section_tag)
time.sleep(1)
  

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #scroll to bottom of the page
time.sleep(1)  

hidden_comm = driver.find_element_by_class_name("hidden-comments-notice")
hidden_comm_button = hidden_comm.find_element_by_tag_name('a').click()



time.sleep(5)


driver.quit()