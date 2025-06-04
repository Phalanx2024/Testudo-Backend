from database.db_controller import DatabaseController
from reports.pdf_scrappers.ningi_research import NingiResearchPDFScraper
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
"Bleecker Street Research"
]

_SHORT_SELLERS_PDF_SCRAPPERS = [
  'Ningi Research'
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
            elif short_seller == "Culper Research":
                for link in links:
                    l =  link[4]
                    report_details = {
                        'report_name': link[2],
                        'report_link': "https:"+l
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