import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport

class CulperScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://culperresearch.com/latest-research"
        )

    def extract_reports(self, page):
        elements = page.query_selector_all('div[data-aid="DOWNLOAD_DOCUMENTS_RENDERED"]')
        
        reports = []
        for element in elements:
            try:
                link_element = element.query_selector('a[data-aid="DOWNLOAD_DOCUMENT_LINK_WRAPPER_RENDERED"]')
                title = link_element.get_attribute('aria-label').replace('Download ', '')
                link = link_element.get_attribute('href')
                date = title.split(' - ')[0]
                
                reports.append(ResearchReport(
                    source=self.url,
                    date=date,
                    title=title,
                    link=link
                ))
                

            except Exception as e:
                logging.error(f"Error processing section: {str(e)}")
                continue
                
        return reports

if __name__ == "__main__":
    reports = CulperScraper().scrape()
    print("\nCulper Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")
