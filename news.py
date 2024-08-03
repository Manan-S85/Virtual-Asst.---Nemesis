import requests
from utilities import takeCommand, speak

def fetch_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    news_headlines = [article['title'] for article in news_data['articles']]
    return news_headlines
