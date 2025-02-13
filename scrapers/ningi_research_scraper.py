import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport

class NingiResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://ningiresearch.com/research/"
        )
    
    def extract_reports(self, page):        
        report_elements = page.query_selector_all('figure.wp-block-table tbody tr:not(:first-child)')
        
        reports = []
        for element in report_elements:
            try:
                cells = element.query_selector_all('td')
                if len(cells) < 4:
                    continue
                
                company = cells[0].inner_text().strip()
                ticker = cells[1].inner_text().strip()
                date = cells[2].inner_text().strip()
                
                link_element = cells[3].query_selector('a')
                link = link_element.get_attribute('href') if link_element else None
                
                if not all([company, date, link]):
                    continue
                
                reports.append(ResearchReport(
                    source=self.url,
                    date=date,
                    title=f"{company} ({ticker})",
                    link=link
                ))
                
            except Exception as e:
                logging.error(f"Error processing table row: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = NingiResearchScraper().scrape()

    print("\nNingi Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}") 