from bs4 import BeautifulSoup
import requests


def fetch_html(url, timeout=10):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching HTML: {e}")
        return None


def extract_main_content(html):
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        tag.decompose()
    
    selectors = [
        'article', '.article-content', '.article-body', 
        '.content-article', '.post-content', '.entry-content',
        'main', '#article', '#content',
    ]
    
    for selector in selectors:
        content = soup.select_one(selector)
        if content:
            return clean_content(content.get_text(separator='\n'))
    
    return clean_content(soup.body.get_text(separator='\n')) if soup.body else ""


def clean_content(text):
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line and len(line) > 1:
            lines.append(line)
    
    return '\n'.join(lines)