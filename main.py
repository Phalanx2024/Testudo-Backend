from research_scrapers import CulperScraper, HunterBrookScraper

def main():
    # Scrape Culper
    culper = CulperScraper()
    culper_reports = culper.scrape()
    
    # Scrape another site
    hunter_brook = HunterBrookScraper()
    hunter_brook_reports = hunter_brook.scrape()
    
    # Print results
    if culper_reports:
        print("\nCulper Reports:")
        for report in culper_reports:
            print(f"\nDate: {report['date']}")
            print(f"Title: {report['title']}")
            print(f"Link: {report['link']}")
    if hunter_brook_reports:
        print("\nHunter Brook Reports:")
        for report in hunter_brook_reports:
            print(f"\nDate: {report['date']}")
            print(f"Title: {report['title']}")
            print(f"Link: {report['link']}")
if __name__ == "__main__":
    main() 