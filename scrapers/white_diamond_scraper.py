import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport

class WhiteDiamondScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://whitediamondresearch.com/"
        )
    
    def extract_reports(self, page):        
        report_elements = page.query_selector_all('article.posts')
        
        reports = []
        for element in report_elements:
            try:
                # Get title and link
                title_element = element.query_selector('h2.research-title a')
                if not title_element:
                    continue
                    
                title = title_element.inner_text().strip()
                link = title_element.get_attribute('href')
                
                # Get date
                date_element = element.query_selector('span.date')
                date = date_element.inner_text().strip() if date_element else None
                
                # Get content preview
                content_element = element.query_selector('div.research-content')
                content = content_element.inner_text().strip() if content_element else None
                
                reports.append(ResearchReport(
                    source=self.url,
                    date=date,
                    title=title,
                    link=link
                ))
                
            except Exception as e:
                logging.error(f"Error processing article: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = WhiteDiamondScraper().scrape()

    print("\nWhite Diamond Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")