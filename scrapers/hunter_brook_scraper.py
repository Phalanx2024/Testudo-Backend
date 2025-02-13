import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport

class HunterBrookScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://hntrbrk.com/category/breaking-news/"
        )
    
    def extract_reports(self, page):        
        report_elements = page.query_selector_all('article.__card')
        
        reports = []
        for element in report_elements:
            try:
                # Get title and link
                link_element = element.query_selector('h2.__h a.__a')
                title = link_element.inner_text().strip()
                link = link_element.get_attribute('href')
                
                # Get date from the time element
                # There are two time elements, we want the first one (date)
                date_element = element.query_selector('time.__byline__seg.__byline__datetime.__u')
                date = date_element.get_attribute('datetime')
                
                # Get authors
                authors = []
                author_elements = element.query_selector_all('.cky-consent-container .cky-notice .cky-notice-group')
                for author_element in author_elements:
                    author_name = author_element.inner_text().strip()
                    authors.append(author_name)
                
                reports.append(ResearchReport(
                    source=self.url,
                    date=date,
                    title=title,
                    link=link,
                ))
                
            except Exception as e:
                logging.error(f"Error processing article: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = HunterBrookScraper().scrape()

    print("\nHunter Brook Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")