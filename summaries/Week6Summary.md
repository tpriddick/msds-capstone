# Week 6 Summary

## Retrospective

### Enjoyable

We were able to finish getting the Twitter/X webscraper able to actually pull data: post content, date of posting, and number of likes. Getting it to actually produce data was immensely satisfying given how difficult it was to set up. Getting the Reddit webscraper has also been relatively easy due to what we learned from getting the Twitter scraper set up.

### Frustrating

Nothing was too frustrating this week other than one point where the Twitter webscraper was pulling reply counts instead of like counts. It turned out this was due to the HTML containers for replies, reposts, and likes having similar structures, and we were calling the first of those three which was the replies.

### Puzzling

Nothing too puzzling, mainly just labor-intensive.

## Planning

Now that we have a better idea of how to scrape, setting up the other webscrapers should (hopefully) be trivial. The next step after this will involve dumping everything into a PostgreSQL database.
