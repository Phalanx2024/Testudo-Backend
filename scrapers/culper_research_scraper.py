import logging
import os
from scrapers.base_scraper import BaseScraper
from models import ResearchReport
from utils.save_reports_to_csv import save_reports_to_csv

class CulperScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://culperresearch.com/latest-research",
            output_filename="culper_reports.csv"
        )
    
    def extract_reports(self, page):
        # Wait for content to load
        page.wait_for_timeout(5000)  # 5 seconds
        
        # Find all download sections
        download_sections = page.query_selector_all('div[data-aid="DOWNLOAD_DOCUMENTS_RENDERED"]')
        
        reports = []
        for section in download_sections:
            try:
                link_element = section.query_selector('a[data-aid="DOWNLOAD_DOCUMENT_LINK_WRAPPER_RENDERED"]')
                title = link_element.get_attribute('aria-label').replace('Download ', '')
                link = link_element.get_attribute('href')
                date = title.split(' - ')[0]
                
                reports.append(ResearchReport(
                    source=self.url,
                    date=date,
                    title=title,
                    link=link
                ))
                
                print("\nCulper Reports:")
                for report in reports:
                    print(f"\nSource: {report.source}")
                    print(f"\nDate: {report.date}")
                    print(f"Title: {report.title}")
                    print(f"Link: {report.link}")

            except Exception as e:
                logging.error(f"Error processing section: {str(e)}")
                continue
                
        return reports

def main():
    culper = CulperScraper()
    culper_reports = culper.scrape()
    if culper_reports:
        save_reports_to_csv(
            culper_reports, 
            "culper_reports.csv", 
            destination_folder=os.path.join(os.path.expanduser('~'), 'Downloads', 'research_reports', 'culper_reports')
        )
        
    print("\nCulper Reports:")
    for report in culper_reports:
        print(f"\nSource: {report.source}")
        print(f"\nDate: {report.date}")
        print(f"Title: {report.title}")
        print(f"Link: {report.link}")

if __name__ == "__main__":
    main() 