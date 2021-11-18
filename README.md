# Project 1: Web scraping and basic summarization

The goal of this Project was to extract posts from the RTVSlo.si or 24ur.com, related to "koronavirus" keyword and visualize data.

## Environment setup. 
You can find more detailed instructions in the Jupyter Notebook while the basic commands for environment setup after installing conda are:

- conda create --name <your_env_name>
- conda activate <your_env_name>
- conda install python
- conda install selenium
- conda install jupyter notebook
- ipython kernel install --name "<your_env_name>" --user
- conda install pandas
- conda install requests
- conda install numpy
- conda install matplotlib
- conda install scipy
- conda install seaborn

## Notebook overwiev
The first part shows more detailed procedure on how to set up the environment. In the second, web scraping part, are detailed descriptions of functions and how data is collected.
The main idea is to first simulate searching by key "koronavirus", collect article URLs into article_urls.txt file, get data from each URL based on the web page specifics, 
store them into the single json file, edit json files and join them into one final data.json file. In third part of notebook are some visualizations from scraped data.

## JSON Schema:

```
[
  {
    "author": ["author_1", "author_2",...],
    "day_published": "DD.MM.YYYY",
    "changed_later": "YES"/"NO", 
    "title": "article_title",
    "subtitle": "article_subtitle",
    "tags": ["tag_1", "tag_2",...],
    "section_tag": "section_tag"
    "content": "article_text",
    "comments": [
        {
            "user": "user_name",
            "date_hour": ["DD.MM.YYYY"; "MM:HH"],
            "grade": comment_grade(int),
            "reply": "YES"/"NO",
            "comment": "comment_text",

        },...
    ],
    "hour_published": "MM:HH"
    
  }, 
  {
    ...
]


```


## Aditional instructions
Scraping can take a lot of time, so be careful when collecting article URLs again and then trying to scrape them. There could also be some new web page formats that weren't included
in my sub 1000 articles and that could trigger some errors. Scraper can aslo check whether some articles were already scraped but unfortunately not by some specific article ID. 
Checking is very useful in case of some interuptions. But after collecting new urls and before trying to scrape them .json files from old ones have to be deleted not to cause any problems.
Old .json files from existing data can be found in single_article_json_files.rar and should be extracted if you don't want to scrape all articles again. 
After extracting data you can delete some of the files, to see how the scraping works, so you don't have to wait that long. 