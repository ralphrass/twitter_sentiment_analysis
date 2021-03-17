# twitter_sentiment_analysis
Twitter API consumption

The script apply the following steps in order to collect tweets from the oficial Twitter API:

1. Authorization and authentication through load_credentials function;
2. Build a sample query to collect specific terms with specific options;
3. Loop through results batches controlling when to hold requests;
4. Store results as CSV and JSON files at each loop and the full result at the end of the main loop.
5. The algorithm tests wheather there is a "next token" available. In case this is positive, the loop keep sending requests. Otherwise, the loop ends.

*Requirements*:

- requests
- pandas
- json
- time
- searchtweets
