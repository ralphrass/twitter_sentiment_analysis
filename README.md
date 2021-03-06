# twitter_sentiment_analysis
Twitter API V2 consumption

Make use of the Twitter Seach Tweets endpoint. See https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction.

The script apply the following steps in order to collect tweets from the oficial Twitter API:

1. Authorization and authentication through load_credentials function;
2. Build a sample query to collect specific terms with specific options;
3. Loop through results batches controlling when to hold requests;
4. Store results as CSV and JSON files at each loop and the full result at the end of the main loop.
5. The algorithm tests wheather there is a "next token" available. In case this is positive, the loop keep sending requests. Otherwise, the loop ends.

*Constraints*

- Max of 100 tweets per request in reverse-chronogical order
- Only the last 7 days tweets (recent search)
- 450 requests per time window (15 min)
- Check https://developer.twitter.com/en/docs/twitter-api/rate-limits

*Premises*

- You have a valid and enabled account in http://developer.twitter.com
- You have a project with an app and a Bearer token activated

*Python requirements*

- requests
- pandas
- json
- time
- searchtweets
