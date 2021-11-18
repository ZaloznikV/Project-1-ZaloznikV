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
import json
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


def get_article_data(site_url):
    """Get data from article in format (authors, title, subtitle, date, hour, change, article_tags, section_tag, text) """
    
    
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=2880,1800')
    options.add_argument("--start-maximized") #so I can see it in fullscreen on laptop
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(site_url)
    
    
    print("Starting to get data from article: ",driver.title)
       
    
    author_class = driver.find_element_by_class_name("author") 
    author_name = author_class.find_element_by_class_name("author-name")
    authors = author_name.text
    #print("Authors are: ", authors)
    time.sleep(1)
    
    authors = list(authors.split(", "))
    
    title_class = driver.find_element_by_class_name("article-header")
    title = title_class.find_element_by_tag_name("h1").text
    subtitle = title_class.find_element_by_class_name("subtitle").text
    #print("Title is: ", title)
    time.sleep(1)
    
    date_class = driver.find_element_by_class_name("publish-meta")
    #print("#########################")
    date_all = list((date_class.text).split("\n")) 
    #print(date_class.text)
    #print(date_all)
    #print(  date_all )
    change = "NO"
    if len(date_all) > 1:
        if "Zadnji poseg:" in date_all[1]:
            change = "YES"
            
    
    date_full = str(date_all[0])
    #print(date_full)
    try:
        date, hour = list(date_full.split(" ob"))
  
    except:
        try:
            date, hour = list(date_full.split(" at")) #some articles in english
        except:
            date, hour = list(date_full.split(" -")) #radio capodistria

        
    #print("Article was published on {}, at {}.".format(date, hour))
    time.sleep(1)
    
    #print("Since publishing article was changed later: {}.".format(change))
    time.sleep(1)
    
    
    article_tags_class = driver.find_element_by_class_name("article-tags")
    articles_tags = article_tags_class.find_elements_by_class_name("tag")
    
    article_tags = []
    
    for article_tag in articles_tags:
        article_tags.append(article_tag.text)
   # print("Article tags are: ", article_tags)
    time.sleep(1)
        
    section_class = driver.find_element_by_class_name("section-title")
    section_tag_a = section_class.find_element_by_tag_name('a')
    section_tag = section_tag_a.get_attribute('aria-label')
    #print("Section tag is: ", section_tag)
    time.sleep(1)
    
    
    body = driver.find_element_by_class_name("article-body")
    bbody = body.find_elements_by_tag_name("p")
    text = []
    for b in bbody:
        text.append(b.text)
    
    text = " ".join(text)

    #print(text)   
    time.sleep(1)
    
    driver.quit()
    #print("########")
    return (authors, title, subtitle, date, hour, change, article_tags, section_tag, text)



#for comments only

def get_article_comments(site_url):
    """Get all comments in format (author, hour_date, grade, text, is_reply)"""
    
    
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=400,1800')
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(site_url)
    
        
                
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    try:
        hidden_comm = driver.find_element_by_class_name("hidden-comments-notice")
        hidden_comm_button = hidden_comm.find_element_by_tag_name('a').click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)


        while True:
            try:
                button_class = driver.find_element_by_id('appcomments')
                buttons = button_class.find_elements_by_css_selector('main div')
                if (buttons[-1].text) != "Prikaži več": #only one or zero page of comments
                    break
                else:
                    show_more = buttons[-1].click() 
                    time.sleep(1)   
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(1)


            except:
                #print("end of comments")
                time.sleep(1)
                break
        all_comments = []   
        comments_class = driver.find_element_by_xpath('//*[@id="appcomments"]/main/div')
        time.sleep(1)
        i = 1
        comments = comments_class.find_elements_by_class_name("comment-container")
        #print("Number of comments is: ", len(comments))
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
            #print(i , "/", len(comments))
            i = i +1
            all_comments.append((author, hour_date, grade, text, reply))
    except:
        all_comments = []
    
    driver.quit()
    return all_comments


def get_data_skit(site_url):
    """Function gets article data from special skit article"""
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=2880,1800')
    options.add_argument("--start-maximized") #so I can see it in fullscreen on laptop
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(site_url)
    
    
    print("Starting to get data from article: ",driver.title)
    
    author_class = driver.find_element_by_id("author") 
    author = author_class.find_element_by_tag_name("span").text
    if author == "":
        author = None
    
    
    date_class = driver.find_element_by_xpath('//*[@id="author"]').text
    date = date_class.split("| ")[1]
    #print(date)
    if date == "":
        date = None
    
    title = driver.find_element_by_class_name("title").text
    if title == "":
        title = None
    subtitle = driver.find_element_by_class_name("subtitle").text
    if subtitle == "":
        subtitle = None
    text_class = driver.find_element_by_class_name("vsebina")
    all_text = text_class.find_elements_by_tag_name("p")
    text = []
    for b in all_text:
        text.append(b.text)
    text = " ".join(text)
    if text == "":
        text = None
    comments = []
    article_tags = []
    section_tag = "SKIT"
    hour = None
    change = None

    driver.quit()
    
    return (author, title, subtitle, date, hour, change, article_tags, section_tag, text, comments)
                
def get_data_dostopno(site_url):
    """Function gets article data from special dostopno article"""
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=2880,1800')
    options.add_argument("--start-maximized") #so I can see it in fullscreen on laptop
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(site_url)
    
    
    print("Starting to get data from article: ",driver.title)
    
    author = driver.find_element_by_class_name("author-name").text
    if author == "":
        author = None
    
    title_header = driver.find_element_by_class_name("article-header")
    title = title_header.find_element_by_tag_name("h1").text
    if title == "":
        title = None
    subtitle =  title_header.find_element_by_tag_name("h3").text
    date_hour_class = driver.find_element_by_css_selector("div header")
    date_hour_ps = date_hour_class.find_elements_by_tag_name('p')
    date_hour = date_hour_ps[-1].text
    date, hour = date_hour.split(" ob")
    if date == "":
        date = None
    if hour == "":
        hour = None
        
    section_tag = "DOSTOPNO"
    article_tags = []
    comments = []
    change = None
    
    text_class = driver.find_element_by_class_name("article")
    all_text = text_class.find_elements_by_tag_name("p")
    text = []
    for b in all_text:
        text.append(b.text)
    text = " ".join(text)
    if text == "":
        text = None
        
    driver.quit()
    
    return (author, title, subtitle, date, hour, change, article_tags, section_tag, text, comments)




def get_data_enostavno(site_url):
    """Function gets article data from special enostavno article"""
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=2880,1800')
    options.add_argument("--start-maximized") #so I can see it in fullscreen on laptop
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(site_url)
    
    
    print("Starting to get data from article: ",driver.title)
    
    author = driver.find_element_by_class_name("author-name").text
    author = author.split(" /")[0]
    if author == "":
        author = None
    
    title_header = driver.find_element_by_class_name("article-header")
    title = title_header.find_element_by_tag_name("h1").text
    if title == "":
        title = None
    subtitle =  title_header.find_element_by_tag_name("h3").text
    date_hour_class = driver.find_element_by_css_selector("div header")
    date_hour_ps = date_hour_class.find_elements_by_tag_name('p')
    date_hour = date_hour_ps[-1].text
    date, hour = date_hour.split(" ob")
    if date == "":
        date = None
    if hour == "":
        hour = None
        
    section_tag = "ENOSTAVNO"
    article_tags = []
    comments = []
    change = None
    
    text_class = driver.find_element_by_class_name("article")
    all_text = text_class.find_elements_by_tag_name("p")
    text = []
    for b in all_text:
        text.append(b.text)
    text = " ".join(text)
    if text == "":
        text = None
        
    driver.quit()
    
    return (author, title, subtitle, date, hour, change, article_tags, section_tag, text, comments)



def make_json_format(authors, title, subtitle, date, hour, change, article_tags, section_tag, text, comments):
    """function that create json file of arguments of single article"""
    line_data = {}
    line_comments = []
    
    line_data["author"] = authors
    line_data["day_published"] = date
    line_data["hour_publishet"] = hour #typo fixed in edited_and_join function
    line_data["changed_later"] = change
    line_data["title"] = title
    line_data["subtitle"] = subtitle
    line_data["tags"] = article_tags
    line_data["section_tag"] = section_tag
    line_data["content"] = text

    for (author, hour_date, grade, text, reply) in comments:
        line_comment = {}
        line_comment["user"] = author
        line_comment["date_hour"] = hour_date #splitted in edited_and_join function
        line_comment["grade"] = grade
        line_comment["reply"] = reply
        line_comment["comment"] = text
        line_comments.append(line_comment)
    line_data["comments"] = line_comments

#        data.append(line_data)
    #print(line_data)
        
    return line_data





def change_day_published(date_published): #just for editing data to be in same format
    """function changes date from DD."month".YYYY do DD.MM.YYYY format"""
    
    dic_month = {"januar": "1", "January": "1", "fabruar": "2", "Fabruary": "2","marec": "3", "March": "3", "april": "4", "April": "4","maj": "5", "May": "5","junij": "6", "June": "6","julij": "7", "July": "7","avgust": "8", "August": "8","september": "9", "September": "9","oktober": "10", "October": "10","november": "11", "November": "11","december": "12", "December": "12", "gennaio": "1", "febbraio": "2","marzo": "3", "aprile": "4","maggio" : "5", "giugno":"6","luglio": "7", "agosto":"8","settembre": "9", "ottobre":"10","novembre": "11", "dicembre": "12","Gennaio": "1", "Febbraio": "2","Marzo": "3", "Aprile": "4","Maggio" : "5", "Giugno":"6","Luglio": "7", "Agosto":"8","Settembre": "9", "Ottobre":"10", "Novembre": "11", "Dicembre": "12"} #slo, eng ita

    
   
    #"23. marec 2021" example
    splitted = date_published.split(" ")
    if len(splitted) > 1: #in format DD. "month" YYYY
        date = date_published.replace(".", "")
        splitted = date.split(" ")
        splitted[1] = dic_month[splitted[1]]
        date_published = ".".join(splitted)
    return date_published
        
        
        
    


def edit_and_join():
    """function for editing some typos in scraped data without having to scrap and wait again"""

    for i in range(1000): #max number of articles that can be obtained from rtvslo
        if os.path.isfile('json/{}.json'.format(i)):
            #print("Working with file: ", i)
        
            a_file = open('json/{}.json'.format(i), "r", encoding='utf-8')
            json_object = json.load(a_file)
            a_file.close()
            #print(json_object)
            
            
            new_comments = []
            json_object["day_published"] = change_day_published( json_object["day_published"] )
            if json_object["hour_publishet"] != None:
                json_object['hour_published'] = json_object.pop("hour_publishet")[1:]
            else:
                json_object['hour_published'] = json_object.pop("hour_publishet")
                json_object['content'] = json_object['content'].replace("\n", "")
                json_object['content'] = json_object['content'].replace('\"', "")

            comments = json_object["comments"]
            if comments != []:
                for comment in comments:
                    date_hour = comment["date_hour"]  
                    splitted = date_hour.split(" ")
                    date = "".join(splitted[1:4])
                    hour = splitted[4]
                    day_month_year = date.split(".") #adjusting month to pandas format
                    if len(day_month_year[0]) == 1:
                        day_month_year[0] = "0" + day_month_year[0]
                    if len(day_month_year[1]) == 1:
                        day_month_year[1] = "0" + day_month_year[1]
                   
                    date = ".".join(day_month_year)
                    comment["date_hour"] = [date, hour]
   
            
            if json_object["day_published"][-1] == ".":
                json_object["day_published"] = json_object["day_published"][:-1]
                
            day_month_year = json_object["day_published"].split(".") #adjusting month to pandas format
            if len(day_month_year[0]) == 1:
                day_month_year[0] = "0" + day_month_year[0]
            if len(day_month_year[1]) == 1:
                day_month_year[1] = "0" + day_month_year[1]
                   
            json_object["day_published"] = ".".join(day_month_year)
                      
            a_file = open('edited_json_files/{}_edited.json'.format(i), "w", encoding='utf-8')
            json.dump(json_object, a_file, ensure_ascii=False)
            a_file.close()
            
    all_data_list = []
    for i in range(1000):
        if os.path.isfile('edited_json_files/{}_edited.json'.format(i)):
            #print("Working with file: ", i)
            a_file = open('edited_json_files/{}_edited.json'.format(i), "r", encoding='utf-8')
            json_object = json.load(a_file)
            a_file.close()
            all_data_list.append(json_object)
    
    #print(all_data_list)
    
    a_file = open('data.json', "w", encoding='utf-8')
    json.dump(all_data_list, a_file , ensure_ascii=False)
    a_file.close()
    return("Done")



        
        