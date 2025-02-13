import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
from datetime import datetime

class ScorpionCapitalScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.scorpioncapital.com/"
        )
    
    def extract_reports(self, page):
        report_elements = page.query_selector_all('figure.sqs-block-image-figure')
        
        reports = []
        for element in report_elements:
            try:
                date_element = element.query_selector('div.image-title')
                if not date_element:
                    continue
                    
                date_text = date_element.inner_text().strip()
                
                subtitle_element = element.query_selector('div.image-subtitle')
                if not subtitle_element:
                    continue
                
                subtitle_texts = subtitle_element.query_selector_all('h3')
                if len(subtitle_texts) < 2:
                    continue
                    
                title = subtitle_texts[0].inner_text().strip()
                description = subtitle_texts[1].inner_text().strip()
                
                link_element = element.query_selector('a[href*=".pdf"]')
                link = link_element.get_attribute('href') if link_element else None
                
                try:
                    date = datetime.strptime(date_text, '%B %d, %Y').strftime('%Y-%m-%d')
                except:
                    date = date_text
                
                reports.append(ResearchReport(
                    source=self.url,
                    date=date,
                    title=title,
                    link=link
                ))
                
            except Exception as e:
                logging.error(f"Error processing report: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = ScorpionCapitalScraper().scrape()

    print("\nScorpion Capital Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")
