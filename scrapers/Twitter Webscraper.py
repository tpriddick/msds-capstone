# Twitter Webscraper

# Importing packages
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import psycopg2
from sqlalchemy import create_engine, text

# Creating connection engine

engine = create_engine("postgresql://postgres:WjValpnjgoYyLCVqoPrZhiSbVwdbgbUh@roundhouse.proxy.rlwy.net:44826/railway")
platform = 'Twitter'

# Defining scroller

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Defining Login
def login_x(username, password, searchterm, ntweets, **kwargs):
    # Defining optional time filter
    # Enter as "YYYY-MM-DD"
    fromdate = kwargs.get('fromdate', None)
    todate = kwargs.get('todate', None)

    # Initializing driver
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(options=options)

    # Open Twitter
    url = 'https://x.com/i/flow/login'
    driver.get(url)

    # Find and input username
    username_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username_input.send_keys(username) # Inputting username
    username_input.send_keys(Keys.ENTER)

    # Find and input password
    password_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # Go to explore
    explore = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div")))
    explore.click()

    # Search with and without time filter
    if np.logical_and(todate != None,fromdate != None):
        # Find search bar and enter search term with date filter
        search = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocapitalize="sentences"]')))
        since = f' since:{fromdate}'
        until = f' until:{todate}'
        search.send_keys(searchterm+since+until)
        search.send_keys(Keys.ENTER) 
    else:
        # Find search bar and enter search term
        search = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocapitalize="sentences"]')))
        search.send_keys(searchterm)
        search.send_keys(Keys.ENTER) 

    latest = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span")))
    latest.click()
    
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
    
    scraped_tweets = []

    while len(scraped_tweets) < ntweets:

        # Find tweets (posts)
        tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
        print('hell yeah')
        for tweet in tweets[:ntweets]:
            try:
                # Get tweet text
                tweet_text_container = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
                spans = tweet_text_container.find_elements(By.CSS_SELECTOR, 'span')
                tweet_text = ''.join([span.text for span in spans])
                
                # Get tweet date
                tweet_date = tweet.find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')

                # Get likes
                try:
                    like_container = tweet.find_element(By.CSS_SELECTOR, 'button[data-testid="like"]')
                    likes = like_container.find_element(By.CSS_SELECTOR, 'span[class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"]').text
                except:
                    # If there are no likes
                    likes = "0"
                
                # Send data to database
                with engine.begin() as trans:
                    trans.execute(text("""
                               INSERT INTO posts (platform, topic, post, likes, date_posted) 
                               VALUES (:platform, :topic, :post, :likes, :date_posted)
                               """),
                          {'platform':platform,
                           'topic':searchterm,
                           'post':tweet_text,
                           'likes':likes,
                           'date_posted':tweet_date})
                
                # Append a dictionary entry to the list
                scraped_tweets.append({
                    "text":tweet_text,
                    "date":tweet_date,
                    "likes": likes
                    })

                if len(scraped_tweets) >= ntweets:
                    break
            except Exception as e:
                print(f"Error extracting tweet: {e}")
        
        # Scroll and load more tweets
        scroll_down(driver)
        time.sleep(2)
    
    for tweet in scraped_tweets:
        print(f"Tweet: {tweet['text']}\nDate: {tweet['date']}\nLikes: {tweet['likes']}\n")
    time.sleep(10)

if __name__ == "__main__":
    your_username = "your_x_username_here"
    your_password = "your_x_password_here"

    login_x("WillametteABGTR","Willamette2024!!",'chipotle',10,fromdate='2024-01-01',todate='2024-06-04')

