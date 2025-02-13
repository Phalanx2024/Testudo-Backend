import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport

class LogPhaseScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.logphase.com"
        )
    
    def extract_reports(self, page):
        report_elements = page.query_selector_all('tbody tr')
        
        reports = []
        for element in report_elements:
            try:
                columns = element.query_selector_all('td')
                if len(columns) < 4:
                    continue
                
                date = columns[1].inner_text().strip()
                
                link_element = columns[2].query_selector('a')
                if not link_element:
                    continue
                    
                title = link_element.inner_text().strip()
                link = link_element.get_attribute('href')

                if link.startswith('/'):
                    link = f"{self.url}{link}"
                
                ticker = columns[3].inner_text().strip()
                
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
    reports = LogPhaseScraper().scrape()

    print("\nLogPhase Research Reports:")
    for report in reports:  
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")
