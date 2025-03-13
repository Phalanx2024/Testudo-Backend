from dataclasses import dataclass
from datetime import date

@dataclass
class ResearchReport:
    source: str
    publication_date: date
    report_title: str
    link: str
    target_company: str
    short_seller: str
    ticker: str = ''
    def to_dict(self) -> dict:
        return {
            # 'source': self.source,
            'publication_date': self.publication_date,
            'report_title': self.report_title,
            'link': self.link,
            'target_company': self.target_company,
            'short_seller': self.short_seller,
            'ticker': self.ticker
        }
    
#              INSERT INTO short_reports (publication_date, report_title, short_seller, last_update, link, target_company, ticker, sector)
#   //       VALUES (${short_report.publication_date},${short_report.report_title}, ${short_report.short_seller}, ${short_report.last_update},
#   //       ${short_report.link}, ${short_report.target_company},${short_report.ticker}, ${short_report.sector})
#   //       ON CONFLICT DO NOTHING;
#   //     `,