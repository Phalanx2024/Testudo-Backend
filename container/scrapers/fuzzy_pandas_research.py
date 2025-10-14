import logging
from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class FuzzyPandaResearchScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://fuzzypandaresearch.com/page/1/"
        )
        self.name = 'Fuzzy Panda Research'
        # self.base_url = "https://fuzzypandaresearch.com/page/"
        # self.total_pages = 2

    def extract_reports(self, page):
        reports = []
        # page_num = 1
        # Scrape multiple pages
        # for page_num in range(0, self.total_pages + 1):
        try:
            # url = f"{self.base_url}{page_num}/"
            # page.goto(url, wait_until='networkidle', timeout=60000)
            # page.wait_for_selector('h2.entry-title')    
            report_elements = page.query_selector_all('header.entry-header')
    
            for report_element in report_elements:
                try:
                    title = report_element.query_selector('h2.entry-title').text_content().strip()
                    date_element = report_element.query_selector('div.date').text_content().strip().split('\n')
                    date_element = [ele.strip() for ele in date_element]
                    datetime_obj = ' '.join(date_element)
                    datetime_obj = datetime.datetime.strptime(datetime_obj, '%d %B, %Y')
                    
                    link = report_element.query_selector('a').get_attribute('href')
                    company_element = report_element.query_selector('div.categories').query_selector('a')
                    company = company_element.text_content().strip()
                        
                    report = ResearchReport(
                        source=link,
                        publication_date=datetime_obj,
                        report_title=title,
                        link=link,
                        target_company=company,
                        short_seller=self.name
                    )
                    reports.append(report)
                        
                except Exception as e:
                    logging.error(f"Error processing report: {e}")
         
        except Exception as e:
            logging.error(f"Error processing page {1}: {e}")
  
                
        # Add missing historical reports
        # historical_reports = [
        #     {
        #         'title': 'Workhorse Group: Active SEC Investigation + Fake Orders + Lost to Two EVs in USPS Bid + New EVs Already Breaking Down = Glue Factory for Workhorse',
        #         'date': datetime.datetime(2021, 1, 9),
        #         'link': 'https://fuzzypandaresearch.com/workhorse-group-sec-investigation-fake-order-book/',
        #         'company': 'Workhorse Group'
        #     },
        #     {
        #         'title': 'Zion Oil & Gas – Financial Times article on undisclosed SEC investigation',
        #         'date': datetime.datetime(2018, 6, 11),
        #         'link': 'https://fuzzypandaresearch.com/zion-oil-gas-ft/',
        #         'company': 'Zion Oil & Gas'
        #     }
        # ]
        
        # for hist_report in historical_reports:
        #     report = ResearchReport(
        #         source=self.base_url,
        #         publication_date=hist_report['date'],
        #         report_title=hist_report['title'],
        #         link=hist_report['link'],
        #         target_company=hist_report['company'],
        #         short_seller=self.name
        #     )
        #     reports.append(report)
            
        return reports

if __name__ == "__main__":
    reports = FuzzyPandaResearchScraper().scrape()
    print("\nFuzzy Panda Research Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")