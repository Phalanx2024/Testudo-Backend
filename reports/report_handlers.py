from database.db_controller import DatabaseController
from reports.pdf_scrappers.ningi_research import NingiResearchPDFScraper
from playwright.sync_api import sync_playwright
_SHORT_SELLERS = [
#   'Kerrisdale Capital',
#   'Hindenburg Research',
#   'Ningi Research'
# "Culper Research"
# "Capybara Research"
# "Dirty Bubble Media",
# "Disclosure Insight",
# "Fuzzy Panda Research"
# "GlassHouse Research"
# "Martin Shkreli"
# "Night Market Research"
# "Outliers Research"
# "Research Ragnarok"
# 'The Bear Cave'
# 'The Captains Log'
# "Unemon"
# "White Diamond Research",
# "Viceroy Research",
# "Spruce Point Management"
# 'Friendly Bear'
# "Sunshine Research"
# "Bonitas Research"
# "Bleecker Street Research"
# 'Scorpion Capital'
# # "Kryptonite Research"
# "HunterBrook Research"
# "Prescience Point",
# "J Capital Research"
 "Wolfpack Research"
# "BMF Reports",
# "Sakura Research"
]

_SHORT_SELLERS_PDF_SCRAPPERS = [
#   'Ningi Research'
]

class ShortReportController:
    def __init__(self):
        self.db = DatabaseController()

    def _get_short_report(self, short_seller_name):
        return self.db.get_link_from_short_sellers(short_seller_name)

    def get_short_reports(self):
        short_reports = {}
        for short_seller in _SHORT_SELLERS:
            links = self._get_short_report(short_seller)
            short_reports_list = []
            if short_seller == "Kerrisdale Capital":
                for link in links:
                    l =  link[4]
                    if l [0]== "'"  and l[-1] == "'":
                        l = l[1:-1]
                    report_details = {
                        'report_name': link[2],
                        'report_link': l
                    }
                    short_reports_list.append(report_details)
            elif short_seller == "J Capital Research":
                for link in links:
                    l =  link[4]
                    report_details = {
                        'report_name': link[2],
                        'report_link': f'https://www.jcapitalresearch.com/{l}',
                    }
                    short_reports_list.append(report_details)
            elif short_seller == "Culper Research":
                for link in links:
                    l =  link[4]
                    report_details = {
                        'report_name': link[2],
                        'report_link': "https:"+l
                        }
                    short_reports_list.append(report_details)

            elif short_seller == "HunterBrook Research":
                with sync_playwright() as p:
                    for link in links:

                        browser = p.chromium.launch(
                            executable_path="/Users/albertzhang/Library/Caches/ms-playwright/chromium_headless_shell-1155/chrome-mac/headless_shell",
                            headless=True,
                        )
                        context = browser.new_context(
                            ignore_https_errors=True,
                            viewport=None,
                            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                        )
                        page = context.new_page()
                        page.goto(link[4])
                        
                        # Wait for the redirect to complete
                        
                        
                        # Get the final URL after redirect (this will be the PDF URL)
                        final_url = page.url

                        report_details = {
                            'report_name': link[2],
                            'report_link': final_url
                            }
                        short_reports_list.append(report_details)
            else:
                for link in links:
                    l =  link[4]
                    report_details = {
                        'report_name': link[2],
                        'report_link': l
                        }
                    short_reports_list.append(report_details)
            short_reports[short_seller] = short_reports_list
        return short_reports



# Issues
# Error fetching content: 404 Client Error: Not Found for url: https://www.disclosureinsight.com/dis-early-signals-report-march-07
# Error fetching content: 404 Client Error: Not Found for url: https://www.disclosureinsight.com/di-watch-list-march-04-2025
# Error fetching content: 404 Client Error: Not Found for url: https://www.disclosureinsight.com/di-watch-list-april-02-2025