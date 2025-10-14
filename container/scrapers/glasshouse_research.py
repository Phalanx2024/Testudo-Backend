import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class GlasshouseResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.glasshouseresearch.com/research.html"
        )
        self.name = 'GlassHouse Research'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all report cells (they contain both date and report info)
            report_cells = page.query_selector_all('td')
            
            for cell in report_cells:
                try:
                    cell_text = cell.text_content().strip()
                    if not cell_text:
                        continue

                    # Extract date using regex (format: "February 7, 2024")
                    date_match = re.search(r'([A-Z][a-z]+ \d{1,2}, \d{4})', cell_text)
                    if not date_match:
                        continue
                        
                    date_str = date_match.group(1)
                    datetime_obj = datetime.datetime.strptime(date_str, '%B %d, %Y')
                    
                    # Extract link
                    link_element = cell.query_selector('a')
                    if not link_element:
                        continue
                        
                    link = link_element.get_attribute('href')
                    if link.startswith('/'):
                        link = f"https://www.glasshouseresearch.com{link}"
                    
                    # Extract company name and ticker
                    title_match = re.search(r'\|(.*?)\|([A-Z]+)', cell_text)
                    title_match = cell.query_selector('a').text_content().split('|')
                    if title_match:
                        company_name = title_match[0].strip()
                        ticker = title_match[1].strip()
                    else:
                        continue
                    
                    # Extract full title (everything after the date)
                    full_title = cell_text.split(ticker)[1].strip()
                    
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj,
                        report_title=full_title,
                        link=link,
                        target_company=company_name,
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                              
                except Exception as e:
                    logging.error(f"Error processing report cell: {e}")
                    
        except Exception as e:
            logging.error(f"Error processing page: {e}")
        
        # For the orddly shaped table this is to remove the empty one
        if len(reports) >= 3:
            reports.pop(2)
        return reports

if __name__ == "__main__":
    scraper = GlasshouseResearchScraper()
    reports = scraper.scrape()
    print("\nGlassHouse Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}")
        print(f"PDF Link: {report.pdf_link}")