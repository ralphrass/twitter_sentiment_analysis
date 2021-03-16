import requests
import pandas as pd
import json
import time
from searchtweets import load_credentials #, ResultStream, gen_request_parameters, collect_results

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    # return os.environ.get("BEARER_TOKEN")
    search_args = load_credentials(yaml_key="search_tweets_v2", env_overwrite=True) # Your Twitter API Key should be stored in user's home directory
    return search_args['bearer_token']


def create_url(next_page=None):
    query = "BancoOriginal picpay -is:retweet -from:BancoOriginal -from:picpay lang:pt" # All tweets about nubank excluding @nubank as a source. No retweets, Pt language only.
    # query = "nubank -is:retweet -from:nubank lang:pt" # All tweets about nubank excluding @nubank as a source. No retweets, Pt language only.
    # Tweet fields are adjustable. # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=entities,source,text,created_at,lang,public_metrics" # possibly_sensitive
    max_results = "max_results=10"
    next_token = ""

    if next_page is not None:
        next_token = "next_token="+next_page

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
        query, tweet_fields, max_results, next_token
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def save_file(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def save_dataframe(file_name, json_data):
    df = pd.json_normalize(json_data, 'data')
    df.text = df.text.apply(lambda x : x.replace('\n', ' '))
    df.to_csv(file_name)
    return df


def main():

    bearer_token = auth()

    df_ltv, next_token = None, None

    for i in range(1, 600): # 3000 * 100 = 300000

        try:
            # Respecting Twitter constraint
            if i%440 == 0:
                print("Wait...")
                time.sleep(960) # 16 min

            url = create_url(next_token)
            headers = create_headers(bearer_token)
            json_response = connect_to_endpoint(url, headers)
            data = json.loads(json.dumps(json_response))

            save_file('readed_json_'+str(i)+'.json', data)
            df = save_dataframe('readed_csv_'+str(i)+'.csv', data)

            if i == 1:
                print("Starting")
                df_ltv = df
            else:
                df_ltv = df_ltv.append(df, ignore_index=True)

            next_token = data['meta']['next_token']
            df_ltv.to_csv('df_ltv_'+str(i)+'.csv', index=False)

        except Exception as e:
            print("Fail...", str(e), e)
            break

    df_ltv.to_csv('df_ltv_final.csv', index=False)


if __name__ == "__main__":
    main()