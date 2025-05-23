# Importing packages
import datetime as dt
import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import psycopg2
from fake_useragent import UserAgent
from sqlalchemy import create_engine, text
from pyvirtualdisplay import Display

# Creating connection engine
engine = create_engine("postgresql://postgres:WjValpnjgoYyLCVqoPrZhiSbVwdbgbUh@roundhouse.proxy.rlwy.net:44826/railway")
platform = 'Twitter'
path = 'screenshot.png'

# Defining random user agent
ua = UserAgent(platforms='pc')
user_agent = ua.random
print(user_agent)

# Starting virtual display
#vdisplay = Display(visible=0,size=(1920,1080))
#vdisplay.start()
#print('Virtual display started')

# Defining scroller
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
# Defining time range
start_date = '2021-07-01'
end_date = '2024-06-30'
dates = pd.date_range(start = start_date, end = end_date)

# Defining Login
def login_x(username, password, searchterm, ntweets, **kwargs):
    # Defining optional time filter
    # Enter as "YYYY-MM-DD"
    fromdate = kwargs.get('fromdate', None)
    todate = kwargs.get('todate', None)
    date_range = kwargs.get('date_range', None)

    # Initializing driver
    options = ChromeOptions()
    options.add_argument("--headless=new")
    #options.add_argument("--start-maximized")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument('--window-size=1920x1080')
    options.add_argument(f'--user-agent={user_agent}')
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(options=options)

    # Open Twitter
    url = 'https://x.com/i/flow/login'
    driver.get(url)
    print("Reached website")

    # Find and input username
    username_input = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    username_input.send_keys(username) # Inputting username
    username_input.send_keys(Keys.ENTER)
    print("Entered username")

    # Find and input password
    password_input = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="current-password"]')))
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    print("Entered password")

    # Go to explore
    explore = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div")))
    print('Explore located')
    time.sleep(3)
    explore.click()
    print('Explore accessed')

    for i in date_range:
        todate = i.date() + dt.timedelta(days=1)
        fromdate = i.date()
        print(f'Searching {searchterm} from {fromdate} to {todate}')
        search = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocapitalize="sentences"]')))
        search.send_keys(Keys.COMMAND + 'a')
        search.send_keys(Keys.DELETE)
        # Search with and without time filter
        if np.logical_and(todate != None,fromdate != None):
            # Find search bar and enter search term with date filter
            search = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocapitalize="sentences"]')))
            print('Search bar located')
            since = f' since:{fromdate}'
            until = f' until:{todate}'
            search.send_keys(searchterm+since+until)
            time.sleep(3)
            search.send_keys(Keys.ENTER)
            print('Searching') 
        else:
            # Find search bar and enter search term
            search = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocapitalize="sentences"]')))
            print('Search bar located')
            search.send_keys(searchterm)
            time.sleep(3)
            search.send_keys(Keys.ENTER) 
            print('Searching')

        #latest = WebDriverWait(driver,50).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div")))
        #print('Trending found')
        #time.sleep(3)
        #latest.click()
        #print('Trending clicked')
        
        WebDriverWait(driver,50).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
        
        scraped_tweets = []

        is_latest_tab = False  # Flag to track if we are on the Latest tab
        max_failed_scrolls = 3  # Define the maximum number of allowed failed scrolls
        failed_scrolls = 0  # Initialize the counter for failed scrolls
        processed_tweet_ids = set()

        while len(scraped_tweets) < ntweets:

            # Find tweets (posts)
            tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')
            print('Tweets found')

            # Track the number of tweets before processing
            initial_tweet_count = len(scraped_tweets)

            for tweet in tweets[:ntweets]:
                if len(scraped_tweets) >= ntweets:
                    break
                try:
                    # Get tweet ID (or another unique attribute)
                    tweet_text_container = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
                    tweet_id = tweet_text_container.get_attribute('id') 
                    print(tweet_id)
                    if tweet_id in processed_tweet_ids:
                        continue  # Skip already processed tweets
                    
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
                        if 'K' in likes:
                            likes = float(likes.replace('K','')) * 1000
                        elif 'M' in likes:
                            likes = float(likes.replace('M','')) * 1000000
                        else:
                            likes = int(likes)
                    except:
                        # If there are no likes
                        likes = "0"
                    # Send data to database
                    with engine.begin() as trans:
                        print('Inserting into database')
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
                    processed_tweet_ids.add(tweet_id)  # Mark tweet as processed
                    print('Initial tweet count:', initial_tweet_count)
                    print('Scraped tweet count:', len(scraped_tweets))
                except Exception as e:
                    print(f"Error extracting tweet: {e}")

            # Check if new tweets were added
            if len(scraped_tweets) == initial_tweet_count:
                failed_scrolls += 1
            else:
                failed_scrolls = 0

            # Switch to the Latest tab after max_failed_scrolls
            if failed_scrolls >= max_failed_scrolls and not is_latest_tab:
                try:
                    latest_tab = WebDriverWait(driver, 50).until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]'))
                    )
                    latest_tab.click()
                    is_latest_tab = True  # Update the flag to indicate we are on the Latest tab
                    failed_scrolls = 0  # Reset the failed scroll counter
                    print('Switched to Latest tab')
                    time.sleep(3)
                    driver.execute_script("window.scrollTo(0, 0);")
                    print('Scrolled to the top')
                except Exception as e:
                    print(f"Error switching to Latest tab: {e}")
                    
            # Scroll and load more tweets
            print('Scrolling')
            scroll_down(driver)
            time.sleep(5)
        
        for tweet in scraped_tweets:
            print(f"Tweet: {tweet['text']}\nDate: {tweet['date']}\nLikes: {tweet['likes']}\n")
        time.sleep(60)

    # Stopping virtual display
    #vdisplay.stop()
    #print('Virtual display stopped')

if __name__ == "__main__":
    your_username = "your_x_username_here"
    your_password = "your_x_password_here"

    login_x("WUABTGR24","Willamette2024!!",'wingstop',250, date_range = dates)
