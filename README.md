# MSDS Capstone: Predicting Stock Market Movements Through Social Media Sentiment Analysis

## Overview

This project explores the use of machine learning and natural language processing to predict stock market movements based on social media sentiment. Our goal is to determine whether signals extracted from platforms like Twitter and Reddit can provide predictive insight into the financial performance of selected companies.

## Project Motivation

Understanding the correlation between public sentiment and market performance has significant business applications. By leveraging social media data, we aim to showcase the power of alternative data sources for financial forecasting and provide tools and insights for investors and organizations.

## Key Research Questions

- Can social media sentiment be reliably used to predict stock price movements?
- What is the correlation between public sentiment (as captured from social media) and the financial performance of companies?
- How can we automate and scale data collection, processing, and analysis for these signals?

## Methods

- **Data Collection:**  
  Automated web scrapers (using Selenium and PRAW) for Twitter and Reddit collect posts related to selected companies (e.g., GameStop, Wingstop, Nvidia, Dogecoin).
- **Data Storage:**  
  Data is stored in PostgreSQL databases and CSV files for analysis.
- **Sentiment Analysis:**  
  Natural language processing techniques are applied to quantify sentiment from the collected posts.
- **Predictive Modeling:**  
  Regression and classification models are built to test the predictive power of sentiment signals on stock price movements.
- **Visualization:**  
  Insights are visualized to communicate findings and model performance.

## Progress & Findings

- Developed scalable web scrapers for Twitter and Reddit.
- Aggregated and cleaned social media and financial data for target companies.
- Applied sentiment analysis and visualized sentiment trends alongside stock price changes.
- Preliminary models show some correlation between sentiment and short-term price movements, but challenges remain with rate limits and data noise.

## Challenges

- Accessing high-quality and high-volume ESG datasets proved difficult, leading to a pivot toward social media-based sentiment analysis.
- Dealing with platform limitations (e.g., Twitter rate limits) and complex HTML structures in web scraping.
- Linking sentiment data to financial performance in a meaningful, statistically robust way.

## Future Work

- Complete sentiment analysis for all data.
- Produce additional visualizations.
- Refine and evaluate predictive models.
- Finalize write-up and presentation.

## Team

- Tyler Gomez Riddick ([LinkedIn](https://www.linkedin.com/in/tyler-gomez-riddick/), [Portfolio](https://www.datascienceportfol.io/tylergomezriddick))
- Aryan Bhardwaj

---

_This repository contains all code, data processing scripts, and documentation for the MSDS capstone project. Please see individual Jupyter notebooks and summaries for detailed analyses and results._
