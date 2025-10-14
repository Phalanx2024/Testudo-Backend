import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime
import re

class GothamCityResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://www.gothamcityresearch.com/main"
        )
        self.name = 'Gotham City Research'
        self.base_url = "https://www.gothamcityresearch.com"

    def extract_reports(self, page):
        reports = []
        
        try:
    
            articles = page.query_selector_all('div.post-list-item-wrapper')
            
            for article in articles:
                try:
                    # Extract title and link
                    title_element = article.query_selector('h2')
                    title = title_element.text_content().strip()
                    link = article.query_selector('a').get_attribute('href')
                    
                    # Extract date from URL or title if available
                    # Most Gotham City Research reports include the date in the title
                    # date_match = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', title)
                    # if date_match:
                    #     date_str = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)}"
                    #     datetime_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
                    # else:
                    #     # Use current date if no date found
                    datetime_obj = datetime.datetime.now()
                    

                    # Extract target company from title
                    company = title.split(':')[0].strip() if ':' in title else title.split('–')[0].strip()
                    
                    report = ResearchReport(
                        source=self.base_url,
                        publication_date=datetime_obj.date(), 
                        report_title=title,
                        link=link,
                        target_company=company,
                        short_seller=self.name
                    )
                    reports.append(report)
                    
                except Exception as e:
                    logging.error(f"Error processing article: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error in extract_reports: {e}")
            
        return reports

if __name__ == "__main__":
    reports = GothamCityResearchScraper().scrape()
    print("\nGotham City Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")
