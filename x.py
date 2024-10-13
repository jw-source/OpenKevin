import tweepy
import re
import requests
from bs4 import BeautifulSoup
import PyPDF2
from io import BytesIO

auth = tweepy.OAuth1UserHandler(
    "pCEOBGkMkS6fv3bkY5eklbfPU", "H0MIWhsj1XKFVX6gLGkZdtGbKJBRF5wDgrU9C1uqzZfMEmRsPN", 
    "1686764374407446528-SQIh85yYXRMdiOClHt7RzqIet2SHXw", "jATA8qBakLkQdXZUOXOnD7vpm7fYq6m82lTkfbOTL0VZf"
)

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAKODwQEAAAAAy8whvvosVfuUCa0AHD1rnOVNGlc%3DENpIFkjy5Q4g7MV2d3C8sLRHSUIIvMlAT8dNKYM2dPPtJ97Kiy")

def extract_urls(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    urls = url_pattern.findall(text)
    return urls

def extract_pdf_text(pdf_content):
    try:
        # Use BytesIO to treat the content as a file-like object
        pdf_file = BytesIO(pdf_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        # Extract text from each page
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            
            # Check if the URL is a PDF
            if 'application/pdf' in content_type or url.endswith('.pdf'):
                return extract_pdf_text(response.content)
            else:
                # For non-PDF URLs, treat it as HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup.get_text(separator=' ', strip=True)
        else:
            return f"Failed to fetch content from {url}, HTTP status: {response.status_code}"
    except requests.RequestException as e:
        return f"Error fetching {url}: {e}"

def search_x_tweets(query, start_time='2024-09-01T00:00:00Z', end_time='2024-10-12T00:00:00Z'):
    query += ' (arxiv.org OR researchgate.net OR ieeexplore.ieee.org OR paperswithcode.com) has:links -is:retweet lang:en'

    tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],
                                    start_time=start_time,
                                    end_time=end_time, max_results=10)
    output = []
    if tweets.data is None:
        return "No tweets found."
    else:
        for tweet in tweets.data:
            tweet_text = tweet.text
            urls = extract_urls(tweet_text)
            
            for url in urls:
                web_content = fetch_url_content(url) 
                if web_content:
                    output.append(web_content)
                else:
                    output.append(f"Could not fetch content from {url}")
        print(output)
        return output

