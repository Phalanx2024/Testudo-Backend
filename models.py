from dataclasses import dataclass
from datetime import date

@dataclass
class ResearchReport:
    source: str
    date: date
    title: str
    link: str
    
    def to_dict(self) -> dict:
        return {
            'source': self.source,
            'date': self.date.isoformat(),
            'title': self.title,
            'link': self.link
        }