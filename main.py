from llm import generate_x_keywords, generate_top_10
from x import search_x_tweets
from clean import clean_output
import time
repo_url = 'https://github.com/kenneth-ge/xAI-Hackathon-Test-Repo'
keywords, repo_info = generate_x_keywords(repo_url)
print(keywords)
relavent_tweets = []
for keyword in keywords:
    relavent_tweets.append(search_x_tweets(keyword))
    time.sleep(1)
output = generate_top_10(repo_info, relavent_tweets)
output = clean_output(output)
print(output)