# Reddit Webscraper

# Importing packages
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Defining Scraping Function
def login_reddit(subreddit, ncomments, topic, **kwargs):
    # Defining topic and kwargs
    top_time = kwargs.get('top_time', None)
    topic_options = ['hot','new','top']
    top_time_options = ['hour','day','week','month','year','all']
    try:
        top_time
    except NameError:
        print('If topic is "top", the time must be specified. Options are "hour", "day", "week", "month, "year", or "all."')
    if topic not in topic_options:
        return('Topic must be "hot","new", or "top".')
    if topic == "top":
        if top_time not in top_time_options:
            return('If topic is "top", the time must be specified. Options are "hour", "day", "week", "month, "year", or "all."')

    # Initializing driver
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(options=options)

    # Open Reddit
    # You do not need an account to access Reddit, so we just need to construct the URL
    url_base = 'https://www.reddit.com/r/'
    topic_constructor = ('/',topic)
    topic_base = ''.join(topic_constructor)
    
    # Constructing if looking at top posts
    if topic == 'top':
        top_time_url = ('/?t=', top_time)
        top_time_base = ''.join(top_time_url)
        top_tuple = (url_base,subreddit,topic_base,top_time_base)
        target = ''.join(top_tuple)
        print(target)
        driver.get(target)
        
    # Constructing if looking at other topics
    else:
        top_tuple = (url_base,subreddit,topic_base)
        target = ''.join(top_tuple)
        print(target)
        driver.get(target)

    # 
    WebDriverWait(driver,20)

if __name__ == "__main__":
    login_reddit('nvidia',10,'top',top_time = 'all')
