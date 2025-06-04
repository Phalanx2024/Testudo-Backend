import requests
from bs4 import BeautifulSoup
import re
import logging
from scrapers.base_scraper import BaseScraper
from models.ResearchReportModel import ResearchReport
import datetime

class JCapitalScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.jcapitalresearch.com/company-reports.html"
        )
        self.name = 'J Capital Research'

    def parse_date(self, date_str):
        """Parse date from various formats and return the latest date if multiple dates exist."""
        try:
            # Split by comma if multiple dates exist
            date_strings = [d.strip() for d in date_str.split(',')]
            dates = []
            
            for d in date_strings:
                try:
                    # Try DD-MMM-YY format (e.g., 27-Jun-23)
                    if '-' in d:
                        # Convert month to proper case (e.g., JUN -> Jun)
                        parts = d.split('-')
                        if len(parts) == 3:
                            month = parts[1].capitalize()
                            d = f"{parts[0]}-{month}-{parts[2]}"
                        date = datetime.datetime.strptime(d, "%d-%b-%y").date()
                    # Try MM/DD/YY format (e.g., 11/21/23)
                    elif '/' in d:
                        parts = d.split('/')
                        if len(parts) == 3:
                            if len(parts[2]) == 2:  # If year is 2 digits
                                year = 2000 + int(parts[2])
                            else:
                                year = int(parts[2])
                            date = datetime.date(year, int(parts[0]), int(parts[1]))
                    else:
                        continue
                    dates.append(date)
                except ValueError as e:
                    logging.warning(f"Could not parse date: {d} - {str(e)}")
                    continue
            
            if dates:
                return max(dates)  # Return the latest date
            return None
            
        except Exception as e:
            logging.error(f"Error parsing date {date_str}: {str(e)}")
            return None

    def extract_reports(self, page):        
        reports = []
        
        try:
            # Get the paragraph element containing all reports
            paragraph = page.query_selector("div.paragraph")
            if not paragraph:
                logging.error("No paragraph element found")
                return reports

            # Split content by <br> tags
            content = paragraph.inner_html()
            report_groups = content.split('<br>')
            
            for group in report_groups:
                try:
                    company_group = group.split('<a href="/')
                    if len(company_group) > 1 :
                        company_name = company_group[0].strip()
                        link = company_group[1].split('">')[0].strip()
                        title = company_group[1].split('">')[1].split('</a>')[0].strip()
                        if '<strong>' in company_group[1]:
                            ticker_date = company_group[1].split('<strong>')[1]
                  
                        else:
                            ticker_date = company_group[1].split('">')[1].split('</a>')[1]
                        if '(' in ticker_date:
                            ticker = ticker_date.split(')')[0].replace('(', '').strip()
                            date = ticker_date.split(')')[1].strip()
                            if '.' in date:
                                date = date.replace('.', '').strip()
                            if '&nbsp;' in date:
                                date = date.replace('&nbsp;', '').strip()
                            if '</span>' in date:
                                date = date.replace('</span>', '').strip()
                            if '</strong>' in date:
                                date = date.replace('</strong>', '').strip()
                            date = self.parse_date(date)
                            if not date:
                                continue
                        elif '</strong>' in ticker_date:
                            ticker = ticker_date.split('</strong>')[0].strip()
                            date = ticker_date.split('</strong>')[1].strip()
                            if '.' in date:
                                date = date.replace('.', '').strip()
                            if '&nbsp;' in date:
                                date = date.replace('&nbsp;', '').strip()
                            if '</span>' in date:
                                date = date.replace('</span>', '').strip()
                            if '</strong>' in date:
                                date = date.replace('</strong>', '').strip()
                            date = self.parse_date(date)
                            if not date:
                                continue
                        else:
                            ticker = None
                            date = ticker_date
                            if '.' in date:
                                date = date.replace('.', '').strip()
                            if '&nbsp;' in date:
                                date = date.replace('&nbsp;', '').strip()
                            date = self.parse_date(date)
                            if not date:
                                continue
                   
                    
                    report = ResearchReport(
                        ticker=ticker,
                        source=self.url,
                        publication_date=date,
                        report_title=title,
                        link=link,
                        target_company=company_name,
                        short_seller=self.name
                    )
                    reports.append(report)
                    
                except Exception as e:
                    logging.error(f"Error processing report group: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {str(e)}")
            
        return reports

if __name__ == "__main__":
    reports = JCapitalScraper().scrape()
    print("\nJ Capital Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
