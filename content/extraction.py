from utils.html_tools import fetch_html, extract_main_content


def get_article_text(url):
    html = fetch_html(url)
    if not html:
        return "Nie udało się pobrać treści artykułu."
    
    return extract_main_content(html)


def extract_article_content(html):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'meta', 'form']):
        tag.decompose()
    
    article_content = None
    selectors = ['article', '.article-body', '.article-content', '.content', '.post', 
                'main', '#article', '#content', '.entry-content']
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            article_content = ' '.join([e.get_text(strip=True) for e in elements])
            if len(article_content) > 100:  # Prawdopodobnie znaleziono treść
                break
    
    if not article_content or len(article_content) < 100:
        article_content = soup.body.get_text(strip=True) if soup.body else soup.get_text(strip=True)
    
    lines = [line.strip() for line in article_content.splitlines() if line.strip()]
    return '\n\n'.join(lines)