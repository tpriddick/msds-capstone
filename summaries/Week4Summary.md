# Week 4 Summary

This past week, we spent most of our time doing background research and trying to hone on the topic of our project, and from there determining the scope. Our final proposal differed from all of the projects outlined in our brainstorming session. We decided, ultimately, to still pursue predicting financial performance, but the subject and means by which we aim to accomplish this differ from our top-rated project.

## Retrospective
### Enjoyable
- Doing background research on a lot of these topics was pretty fun. We toyed around with other project ideas not included in our brainstorming submission such as using NASA's Prognostics Datasets to build a predictive maintenance model, using Bitcoin blockchain data to perform anomaly detection, and analyzing customer subscription data to analyze customer churn.
- Writing the project proposal was enjoyable as it gave us a chance to toy around with fun ideas around how we could use sentiment analysis to predict stock market movement.

### Frustrating
- Our original project idea revolved around attempting to predict stock market moment movements using ESG (Environmental, social, and governmental) data. We spent a significant amount of time trying to find current and comprehensive ESG datasets, but almost all of them require some form of paid subscription. This required us to pivot.
- Trying to find the tools we need for this project was somewhat frustrating.

### Puzzling
- The social media webscraping is going to involve tools that we have not used before: PRAW (Python Reddit API Wrapper) and Selenium. This is going to require some learning at the top.
- In order to move forward, we need to make sure that we can actually set up the webscrapers the way we are hoping.
- We also need to ensure that we can link our financial data to our social media sentiment data.

## Planning
As a data science team, we would like to setup (using PRAW for Reddit and Selenium for everything else) and automate (via Docker and Railway) our social media webscrapers for current and past posts for the list of companies (GameStop, WingStop, etc.), as well as collect financial data from Yahoo and Google finance so that we can pull the data into a database.

### Acceptance Criteria
- A set of webscrapers that scrape data from social media websites at set intervals every day
  - Social media data should be accessible via a PostgreSQL database or set of CSVs
- CSV files containing financial data about selected companies
