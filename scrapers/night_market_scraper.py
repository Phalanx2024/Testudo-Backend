import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport

class NightMarketScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://nightmarketresearch.com"
        )
    
    def extract_reports(self, page):
        report_elements = page.query_selector_all('p.has-text-color.has-link-color')
        
        reports = []
        for element in report_elements:
            try:
                link_element = element.query_selector('a')
                if not link_element:
                    continue
                    
                title = link_element.inner_text().strip()
                link = link_element.get_attribute('href')
                
                # Find the next sibling p tag with the date
                date_element = element.query_selector('+ p.has-foreground-light-color')
                if not date_element:
                    continue
                    
                date = date_element.inner_text().strip().replace('Published ', '').replace('em>', '')
                
                if link.startswith('/'):
                    link = f"{self.url}{link}"
                
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
    reports = NightMarketScraper().scrape()
    
    print("\nNight Market Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}") 