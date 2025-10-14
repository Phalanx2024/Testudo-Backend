import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class BMFReportsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://bmfreports.com/articles"
        )
        self.name = 'BMF Reports'

    def extract_reports(self, page):
        reports = []
        
        try:
            # Based on the website structure, reports appear to be in sections
            # Look for report entries using query_selector
            report_sections = page.query_selector_all('a')
            
            for section in report_sections:
                try:
                    # Look for title elements
                    title_element = section.query_selector('h2')
                    if not title_element:
                        continue
                        
                    title = title_element.text_content().strip()
                    if not title or len(title) < 10:  # Skip very short titles
                        continue
                    
                    # Look for links in the section
        
                    link = section.get_attribute('href')
                    link = "https://bmfreports.com" + link.split(".")[1]
                    # Extract ticker from title
                    ticker = ''
                    if '(' in title and ')' in title:
                        # Extract ticker from parentheses
                        ticker_match = re.search(r'\(([^)]+)\)', title)
                        if ticker_match:
                            ticker = ticker_match.group(1)
                    elif '$' in title:
                        # Extract ticker after dollar sign
                        ticker_match = re.search(r'\$([A-Z]+)', title)
                        if ticker_match:
                            ticker = ticker_match.group(1)
                    
                    # Look for date elements
         
                    date_element = section.query_selector_all('p[data-styles-preset ="o7K7mMoMe"]')
                    date_element = date_element[-1]
                    if date_element:
                        date_text = date_element.text_content().strip()
                        if date_text:
                            try:
                                # Try to parse various date formats
                                if ',' in date_text:
                                    # Format like "June 27, 2025"
                                    date_obj = datetime.datetime.strptime(date_text, "%B %d, %Y").date()
                                elif len(date_text.split()) == 2:
                                    # Format like "Jun 27"
                                    current_year = datetime.datetime.now().year
                                    date_with_year = f"{date_text} {current_year}"
                                    date_obj = datetime.datetime.strptime(date_with_year, "%b %d %Y").date()
                            except Exception as e:
                                logging.warning(f"Could not parse date '{date_text}': {e}")
                    
                    # Create the report object
                    report = ResearchReport(
                        source=self.url,
                        publication_date=date_obj,
                        report_title=title,
                        link=link,
                        target_company=ticker,
                        short_seller=self.name,
                        ticker=ticker
                    )
                    reports.append(report)
                        
                except Exception as e:
                    logging.error(f"Error processing report section: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error processing BMF Reports page: {e}")
            
        return reports

if __name__ == "__main__":
    scraper = BMFReportsScraper()
    reports = scraper.scrape()
    print("\nBMF Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
        print(f"Ticker: {report.ticker}") 