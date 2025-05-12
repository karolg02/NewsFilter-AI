import feedparser
from bs4 import BeautifulSoup


def clean_html(text):
    return BeautifulSoup(str(text), "html.parser").get_text().strip()


def get_feed_count(link_url):
    try:
        headers = {'User-Agent': 'NewsFilterAI/1.0'}
        feed_data = feedparser.parse(link_url, request_headers=headers)
        
        if feed_data.bozo:
            pass
        return len(feed_data.entries)
    except Exception as e:
        print(f"Error fetching feed count for {link_url}: {e}")
        return 0


def parse_feed(url, source_name=None):
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            title = entry.title
            summary = entry.get("summary") or entry.get("description") or ""
            link = entry.link
            date = entry.get("published", "") or entry.get("updated", "")
            summary = clean_html(summary)
            articles.append({
                "title": title,
                "summary": summary,
                "link": link,
                "date": date,
                "source": source_name
            })
        return articles
    except Exception as e:
        print(f"Error parsing feed {url}: {e}")
        return []


def fetch_feed(url):
    """Pobiera dane z pojedynczego źródła RSS i zwraca DataFrame"""
    import pandas as pd
    
    articles = parse_feed(url)
    if articles:
        return pd.DataFrame(articles)
    else:
        return pd.DataFrame(columns=["title", "summary", "link", "date", "source"])


def download_feeds_to_dataframe(feeds):
    import pandas as pd
    
    all_articles = []
    for name, url in feeds:
        articles = parse_feed(url, name)
        all_articles.extend(articles)
    
    if all_articles:
        df = pd.DataFrame(all_articles)
        return df
    else:
        return pd.DataFrame(columns=["title", "summary", "link", "date", "source"])