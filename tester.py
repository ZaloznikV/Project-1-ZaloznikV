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




def links(MAIN_URL,search_KEY, n):
    """Returns list of n urls"""

 

    PATH = r"chromedriver.exe"
    

    options = webdriver.ChromeOptions()
    
    options.add_argument('window-size=2880,1800')
    options.add_argument("--start-maximized") #so I can see it in fullscreen on laptop
    driver = webdriver.Chrome(PATH, options=options)
    driver.set_window_size(2880, 1800)
    driver.maximize_window()


    driver.get(MAIN_URL)

    print("Starting to get articles URLs from page: ",driver.title)

    search = driver.find_element_by_id("header-search-input") #search for key word
    search.send_keys(search_KEY)
    search.send_keys(Keys.RETURN)

    time.sleep(5)

    i = 1 #page counter
    j = 1
    URLS = [] #list of all urls

    while (len(URLS)< n - 11): #max number of articles
        articles = driver.find_elements_by_class_name("article-archive-item")
        time.sleep(1)
        print("I'm on page: {}".format(i))
        i = i + 1
        for article in articles:
            items = article.find_element_by_css_selector('div a')
            print(j, items.get_attribute('href'))
            j = j + 1
            time.sleep(1)
            URLS.append(items.get_attribute('href'))
        #print(URLS)   
        #print("########################")

        time.sleep(1)  
        driver.execute_script("window.scrollTo(0, 1800)") #scroll to bottom of the page
        time.sleep(1)

        paginator = driver.find_elements_by_css_selector("nav ul li")

        last_page = paginator[-1]
        last_page.click() #click to go to next page

    URLS = URLS[1::] #first is not article
    with open('article_urls.txt', 'w') as f: #write URLs to file
        for url in URLS:
            f.write("%s\n" % url)

    driver.quit()








PATH = r"chromedriver.exe"
file = open('article_urls.txt', 'r')
Lines = file.readlines()


# for line in Lines:
#     print(line)
#     time.sleep(1)
#prvega je potrebno ignorirati ker ni novica ampak podstran
site_url = "https://www.rtvslo.si/slovenija/skupaj-naprej-v-premagovanje-epidemije/600811"
#site_url = line potem ko bo v for zanki

def get_article_data(site_url):
    """Get data from article in format (authors, title, subtitle, date, hour, change, article_tags, section_tag) """
    
    
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
    subtitle = title_class.find_element_by_class_name("subtitle").text
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
      
    
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #scroll to bottom of the page
    # time.sleep(1)  
    
    # hidden_comm = driver.find_element_by_class_name("hidden-comments-notice")
    # hidden_comm_button = hidden_comm.find_element_by_tag_name('a').click()
    
    
    time.sleep(1)
    
    driver.quit()
    print("########")
    return (authors, title, subtitle, date, hour, change, article_tags, section_tag)



#for comments only

def get_article_comments(site_url):
    """Get all comments in format (author, hour_date, grade, text, is_reply) """
    
    
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=400,1800')
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(site_url)
    
        
                
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    hidden_comm = driver.find_element_by_class_name("hidden-comments-notice")
    hidden_comm_button = hidden_comm.find_element_by_tag_name('a').click()
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    
    print("bla")
    while True:
        try:
            button_class = driver.find_element_by_id('appcomments')
            buttons = button_class.find_elements_by_css_selector('main div')
            show_more = buttons[-1].click() 
            time.sleep(1)   
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            
        
        except:
            print("end of comments")
            time.sleep(1)
            break
    all_comments = []   
    comments_class = driver.find_element_by_xpath('//*[@id="appcomments"]/main/div')
    time.sleep(5)
    i = 1
    comments = comments_class.find_elements_by_class_name("comment-container")
    print("Number of comments is: ", len(comments))
    for comment in comments[3::]:

        splitted = comment.text.split("\n")
        #print(splitted)
        author = splitted[0]
        hour_date = splitted[1]
        try:
            grade = int(splitted[2].split(" ")[0])
            if len(splitted) > 6:    
                text = "".join(splitted[3:-2])
            else:
                text = splitted[3]
            reply = "NO"
        except:
            reply_to = splitted[2]
            grade = str(int(splitted[3].split(" ")[0]))
            if len(splitted) > 6:
                text = "".join(splitted[4:-2])
            else:
                text = splitted[4]
            reply = "YES"
        #print(author, hour_date, grade, text, reply)
        print(i , "/", len(comments))
        i = i +1
        all_comments.append((author, hour_date, grade, text, reply))
            
    
    driver.quit()
    return all_comments