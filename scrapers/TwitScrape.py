import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import pandas as pd
import datetime as dt
import psycopg2
from sqlalchemy import create_engine, text
import time
from random import randint

async def main(searchterm,fromdate,todate):
    engine = create_engine("postgresql://postgres:WjValpnjgoYyLCVqoPrZhiSbVwdbgbUh@roundhouse.proxy.rlwy.net:44826/railway")
    platform = 'Twitter'
    api = API()
    dates = pd.date_range(start = fromdate, end = todate)

    for day in dates:
        qfrom = f'since:{day.date()}'
        nextday = day + dt.timedelta(days=1)
        qto = f'until:{nextday.date()}'

        # Constructing the searchterm
        query_constructor = searchterm+' '+qfrom+' '+qto
        print('Searching', query_constructor)
        tweetcount = 0
        async for tweet in api.search(query_constructor,limit=500):
            with engine.begin() as trans:
                if tweetcount == 50:
                    print('Inserting into database')
                    tweetcount = 0
                    time.sleep(randint(5,15))
                trans.execute(text("""
                                    INSERT INTO posts (platform, topic, post, likes, date_posted) 
                                    VALUES (:platform, :topic, :post, :likes, :date_posted)
                                 """),
                        {'platform':platform,
                        'topic':searchterm,
                        'post':tweet.rawContent,
                        'likes':tweet.likeCount,
                        'date_posted':tweet.date})
                tweetcount += 1

if __name__ == "__main__":
    asyncio.run(main('gamestop','2020-02-16','2020-12-31'))
