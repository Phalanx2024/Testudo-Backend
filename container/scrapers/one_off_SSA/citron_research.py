from scrapers.base_scraper import BaseScraper
from model.ResearchReportModel import ResearchReport
import datetime

class CitronResearchcraper(BaseScraper):
    def __init__(self):
        super().__init__(
            url="https://citronresearch.com/"  # You'll need to verify this URL
        )
        self.name = 'Citron Research'
        
    def get_static_reports(self):
        reports_data = [
        # 2020
            {
                "title": "Peloton Research Report",
                "date": datetime.datetime(2020, 1, 1),
                "company": "Peloton",
                "link": "https://citronresearch.com/"
            },
            # 2019
            {
                "title": "Fleetcor Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Fleetcor",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Peloton Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Peloton",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Wayfair Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Wayfair",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Bausch Health Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Bausch Health",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "McKesson Research Report",
                "date": datetime.datetime(2019, 1, 1),
                "company": "McKesson",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Enphase and Solaredge Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Enphase and Solaredge",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Grand Canyon Education Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Grand Canyon Education",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "General Electric Report",
                "date": datetime.datetime(2019, 1, 1),
                "company": "General Electric",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Markopolos Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Markopolos",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Invitae Research Report",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Invitae",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Revolve Group Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Revolve Group",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Amedisys Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Amedisys",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Village Farms Research",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Village Farms",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Lyft Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Lyft",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Shopify Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Shopify",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Chegg Research Report",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Chegg",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Inogen Analysis",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Inogen",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Twitter Investigation",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Twitter",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Ligand Pharmaceuticals Research",
                "date": datetime.datetime(2019, 1, 1),
                "company": "Ligand Pharmaceuticals",
                "link": "https://citronresearch.com/"
            },
                    # 2018
            {
                "title": "Facebook Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Facebook",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Twitter Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Twitter",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Aphria Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Aphria",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Mallinckrodt Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Mallinckrodt",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "NIO Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "NIO",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Wayfair Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Wayfair",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Tesla Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Tesla",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Polarityte Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Polarityte",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Pyrus International Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Pyrus International",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Namaste Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Namaste",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Tilray Management Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Tilray Management",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Cronos Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Cronos",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Nvidia Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Nvidia",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Abbvie Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Abbvie",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Netflix Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Netflix",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Fitbit Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Fitbit",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Snap Inc Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Snap Inc",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Roku Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Roku",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Alibaba Research Report",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Alibaba",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Hailing Education Analysis",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Hailing Education",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Facebook and Shopify Investigation",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Facebook and Shopify",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Exact Sciences Corp Research",
                "date": datetime.datetime(2018, 1, 1),
                "company": "Exact Sciences Corp",
                "link": "https://citronresearch.com/"
            },
                    # 2017
            {
                "title": "Shopify Analysis",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Shopify",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Mimedx Investigation",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Mimedx",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Ubiquiti Research Report",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Ubiquiti",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "GBTC Analysis",
                "date": datetime.datetime(2017, 1, 1),
                "company": "GBTC",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Motorola Solutions Investigation",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Motorola Solutions",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Acthar Research Report",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Acthar",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Wayfair Analysis",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Wayfair",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Nvidia Investigation",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Nvidia",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Mallinckrodt Research Report",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Mallinckrodt",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Blackberry Analysis",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Blackberry",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Exact Sciences Corp Investigation",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Exact Sciences Corp",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Fleetcor Research Report",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Fleetcor",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Transdigm Analysis",
                "date": datetime.datetime(2017, 1, 1),
                "company": "Transdigm",
                "link": "https://citronresearch.com/"
            },
            # 2016
            {
                "title": "Express Scripts Investigation",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Express Scripts",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Transdigm Research Report",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Transdigm",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Lannet Analysis",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Lannet",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Avexis Investigation",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Avexis",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Cyberdyne Research Report",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Cyberdyne",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Mallinckrodt Analysis",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Mallinckrodt",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Alliance Data Systems Investigation",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Alliance Data Systems",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Chemours Research Report",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Chemours",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Intrexon Analysis",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Intrexon",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Mobileye Investigation",
                "date": datetime.datetime(2016, 1, 1),
                "company": "Mobileye",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "J2 Global JCOM Research Report",
                "date": datetime.datetime(2016, 1, 1),
                "company": "J2 Global JCOM",
                "link": "https://citronresearch.com/"
            },
                    # 2015
            {
                "title": "Monster Beverage Analysis",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Monster Beverage",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Valeant Investigation",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Valeant",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Twou Research Report",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Twou",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Mobileye and Volkswagen Analysis",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Mobileye and Volkswagen",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Wayfair Investigation",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Wayfair",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Ambarella Research Report",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Ambarella",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Zillow Analysis",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Zillow",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Lumber Liquidators Investigation",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Lumber Liquidators",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Accelerate Diagnostics Research",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Accelerate Diagnostics",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Gopro Analysis",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Gopro",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Textura Investigation",
                "date": datetime.datetime(2015, 1, 1),
                "company": "Textura",
                "link": "https://citronresearch.com/"
            },
            # Reports with NA dates
            {
                "title": "Terra Nostra Resources Investigation",
                "date": None,
                "company": "Terra Nostra Resources",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Hearatlast Research Report",
                "date": None,
                "company": "Hearatlast",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Home Solutions America Analysis",
                "date": None,
                "company": "Home Solutions America",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "GTX Global Investigation",
                "date": None,
                "company": "GTX Global",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "YP.net Research Report",
                "date": None,
                "company": "YP.net",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China Medical Corp Analysis",
                "date": None,
                "company": "China Medical Corp",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China Finance Online Investigation",
                "date": None,
                "company": "China Finance Online",
                "link": "https://citronresearch.com/"
            },
                    {
                "title": "Zillow Trulia Analysis",
                "date": None,
                "company": "Zillow Trulia",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Usana Investigation",
                "date": None,
                "company": "Usana",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Bank of the Internet and AXOS Bank Research",
                "date": None,
                "company": "Bank of the Internet and AXOS Bank",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Blackberry Analysis",
                "date": None,
                "company": "Blackberry",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Questcor Investigation",
                "date": None,
                "company": "Questcor",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Plug Power Research",
                "date": None,
                "company": "Plug Power",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Medbox Analysis",
                "date": None,
                "company": "Medbox",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Sodastream Investigation",
                "date": None,
                "company": "Sodastream",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "3D Systems Research",
                "date": None,
                "company": "3D Systems",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Organovo Analysis",
                "date": None,
                "company": "Organovo",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Textura Investigation",
                "date": None,
                "company": "Textura",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Garmin Research",
                "date": None,
                "company": "Garmin",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Agritech Analysis",
                "date": None,
                "company": "Agritech",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Amedisys Investigation",
                "date": None,
                "company": "Amedisys",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Life Partners, Inc Research",
                "date": None,
                "company": "Life Partners, Inc",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "World Acceptance Corp Analysis",
                "date": None,
                "company": "World Acceptance Corp",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Cbeyond Investigation",
                "date": None,
                "company": "Cbeyond",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Vistaprint Research",
                "date": None,
                "company": "Vistaprint",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "International Bancshares Corp Analysis",
                "date": None,
                "company": "International Bancshares Corp",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "New Oriental Education and Technology Investigation",
                "date": None,
                "company": "New Oriental Education and Technology",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Tesla Research",
                "date": None,
                "company": "Tesla",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Intuitive Surgical Management Analysis",
                "date": None,
                "company": "Intuitive Surgical Management",
                "link": "https://citronresearch.com/"
            },
                    {
                "title": "Qihoo 360 Technology Analysis",
                "date": None,
                "company": "Qihoo 360 Technology",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China Mediaexpress Investigation",
                "date": None,
                "company": "China Mediaexpress",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Harbin Electric Research",
                "date": None,
                "company": "Harbin Electric",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Zagg Analysis",
                "date": None,
                "company": "Zagg",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China Biotics Investigation",
                "date": None,
                "company": "China Biotics",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Longstop Financial Research",
                "date": None,
                "company": "Longstop Financial",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "MOBI Analysis",
                "date": None,
                "company": "MOBI",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Lithium Exploration Investigation",
                "date": None,
                "company": "Lithium Exploration",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Deer Consumer Products Research",
                "date": None,
                "company": "Deer Consumer Products",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China Media Express Analysis",
                "date": None,
                "company": "China Media Express",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Whitin Trust USA Investigation",
                "date": None,
                "company": "Whitin Trust USA",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China Value Technology Research",
                "date": None,
                "company": "China Value Technology",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Great Northern Iron Analysis",
                "date": None,
                "company": "Great Northern Iron",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Horigoshi Worldwide Investigation",
                "date": None,
                "company": "Horigoshi Worldwide",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Uranium Energy Research",
                "date": None,
                "company": "Uranium Energy",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Frazer Frost Analysis",
                "date": None,
                "company": "Frazer Frost",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "China New Borun Investigation",
                "date": None,
                "company": "China New Borun",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Angie's List Research",
                "date": None,
                "company": "Angie's List",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Unipixel Analysis",
                "date": None,
                "company": "Unipixel",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Nu Skin Investigation",
                "date": None,
                "company": "Nu Skin",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Vivus Research",
                "date": None,
                "company": "Vivus",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Sinocooking Analysis",
                "date": None,
                "company": "Sinocooking",
                "link": "https://citronresearch.com/"
            },
            {
                "title": "Seabridge Investigation",
                "date": None,
                "company": "Seabridge",
                "link": "https://citronresearch.com/"
            }
        ]

        reports = []
        for report in reports_data:
            if report["date"] is None:
                re = ResearchReport(
                    source=self.url,
                    publication_date=None,
                    report_title=report["title"],
                    link=report["link"],
                    target_company=report["company"],
                    short_seller=self.name
            )
                reports.append(re)
            else :  
                re = ResearchReport(
                source=self.url,
                publication_date=report["date"].date(),
                report_title=report["title"],
                link=report["link"],
                target_company=report["company"],
                short_seller=self.name
            )
                reports.append(re)

        return reports

    def extract_reports(self, page):
        # Since this is a static list, we don't need to scrape the page
        return self.get_static_reports()

if __name__ == "__main__":
    reports = CitronResearchcraper().scrape()
    print("\nQuintessential Capital Reports:")
    for report in reports:
        print(f"\nSource: {report.source}")
        print(f"Date: {report.publication_date}")
        print(f"Title: {report.report_title}")
        print(f"Link: {report.link}")
        print(f"Target Company: {report.target_company}")
        print(f"Short Seller: {report.short_seller}")