import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class AnathemaResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://anathemaresearch.com/"
        )
        self.name = 'Anathema Research'
        self.base_url = "https://anathemaresearch.com"

    def extract_reports(self, page):
        reports = []
        
        try:
            # Find all research sections
            sections = page.query_selector_all('div[class*="uk-card uk-card-secondary uk-card-body"]')
            
            for section in sections:
                try:
                    # Get date from p element
                    date_element = section.query_selector('p')
                    if not date_element:
                        continue
                        
                    date_text = date_element.text_content().strip()
                    try:
                        # Parse date in format "Sep 19, 2023"
                        datetime_obj = datetime.datetime.strptime(date_text, '%b %d, %Y')
                    except ValueError:
                        logging.error(f"Could not parse date: {date_text}")
                        continue
                    
                    # Get title
                    title = section.query_selector('h4').text_content().strip()
                    
                    # Extract ticker (format: NASDAQ: TROO)
                    ticker = ""
                    company_name = ""
                    ticker_match = re.search(r'\(((?:NASDAQ|NYSE|OTC):\s*([A-Z]+))\)', title)
                    if ticker_match:
                        ticker = ticker_match.group(2)
                        # Get company name from before the ticker
                        company_parts = title.split('(')[0].strip()
                        if 'We are short' in company_parts:
                            company_name = company_parts.split('We are short')[1].strip()
                        else:
                            company_name = company_parts
                    
                    # Get link
                    link_element = section.query_selector_all('a')[-1] if section.query_selector_all('a') else None
                    link = link_element.get_attribute('href') if link_element else self.url
                    
                    report = ResearchReport(
                        source=self.url,
                        publication_date=datetime_obj.date(),
                        report_title=title,
                        link=link,
                        target_company=company_name,
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                    logging.info(f"Found report: {title} ({datetime_obj.date()})")
                    
                except Exception as e:
                    logging.error(f"Error processing section: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = AnathemaResearchScraper()
    reports = scraper.scrape()
    print("\nAnathema Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Ticker: {report.ticker}")
        print(f"Short Seller: {report.short_seller}") 