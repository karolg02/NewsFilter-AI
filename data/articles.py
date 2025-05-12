from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class Article:
    title: str
    summary: str
    link: str
    date: str
    source: str
    label: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        return cls(
            title=data.get('title', ''),
            summary=data.get('summary', ''),
            link=data.get('link', ''),
            date=data.get('date', ''),
            source=data.get('source', ''),
            label=data.get('label')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'summary': self.summary,
            'link': self.link,
            'date': self.date,
            'source': self.source,
            'label': self.label
        }
    
    @property
    def formatted_date(self) -> str:
        try:
            for date_format in ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%m/%d/%y %H:%M']:
                try:
                    dt = datetime.strptime(self.date, date_format)
                    return dt.strftime('%d-%m-%Y %H:%M')
                except ValueError:
                    continue
            return self.date
        except:
            return self.date


class ArticleCollection:
    def __init__(self, articles: List[Article]):
        self.articles = articles
    
    @classmethod
    def from_dataframe(cls, df) -> 'ArticleCollection':
        articles = [Article.from_dict(row) for _, row in df.iterrows()]
        return cls(articles)
    
    def filter_by_source(self, source: str) -> 'ArticleCollection':
        filtered = [a for a in self.articles if a.source == source]
        return ArticleCollection(filtered)
    
    def search(self, query: str) -> 'ArticleCollection':
        query = query.lower()
        results = [a for a in self.articles if 
                  query in a.title.lower() or 
                  (a.summary and query in a.summary.lower())]
        return ArticleCollection(results)
    
    def to_list_of_dicts(self) -> List[Dict[str, Any]]:
        return [article.to_dict() for article in self.articles]