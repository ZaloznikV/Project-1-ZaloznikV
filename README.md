# Project 1: Web scraping and basic summarization

The goal of this Project is to extract posts from the RTVSlo.si or 24ur.com, related to "koronavirus" keyword and visualize data.

## Environment setup. 
More detailed instructioins are in notebook but basic commands for environment setup after installing conda are:

- conda create --name <your_env_name>
- conda activate <your_env_name>
- conda install python
- conda install selenium
- conda install jupyter notebook
- ipython kernel install --name "<your_env_name>" --user
- conda install pandas
- conda install requests

## Notebook overwiev
In the first part is more detailed procedure how to set up environment. In second, web scraping part, is detailed descriptions of functions and how is data collected.
But main idea is to first simulate searching by key "koronavirus", collect articles urls into article_urls.txt file , get data from each url based on web page specifics, 
store it into single json file, edit json files and join them into one final data.json file. In third part of notebook are some visualizations from scraped data.


## Aditional instructions
Scraping can take a lot of time so be carefull when collecting article urls again and then trying to scrape them. There could also be some new web page formats that were missed
in my sub 1000 articles and so could trigger some errors. Scraper also checks whether some articles were already scraped but unfortunately not by some specific article ID. 
Checking is very useful in case of some interuptions. But after collecting new urls and trying to scrape them .json files from old ones have to be deleted not to cause any problems.