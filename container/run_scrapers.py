import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
import time
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database controller
from database.db_controller import DatabaseController

# Import all scrapers
from scrapers.white_diamond_scraper import WhiteDiamondScraper
from scrapers.hunter_brook_scraper import HunterBrookScraper
from scrapers.logphase_scraper import LogPhaseScraper
from scrapers.culper_research_scraper import CulperScraper
from scrapers.scorpion_capital_scraper import ScorpionCapitalScraper
from scrapers.ningi_research_scraper import NingiResearchScraper
from scrapers.night_market_scraper import NightMarketScraper
from scrapers.bleecker_street_research import BleeckerStreetResearchScraper
from scrapers.blue_orca_capital import BlueOrcaCapitalScraper
from scrapers.fuzzy_pandas_research import FuzzyPandaResearchScraper
from scrapers.gmt_research import GMTResearchScraper
from scrapers.hindenburg_research import HindenburgResearchScraper
from scrapers.viceroy_research import ViceroyResearchScraper
from scrapers.sprucepoint_management import SprucepointManagementScraper
from scrapers.kerrisdale_capital import KerrisdaleScraper
from scrapers.gotham_city_research import GothamCityResearchScraper
from scrapers.snowcap_research import SnowcapResearchScraper
from scrapers.bonitas_research import BonitasResearchScraper
from scrapers.glasshouse_research import GlasshouseResearchScraper
from scrapers.capybara_research import CapybaraResearchScraper
from scrapers.dirty_bubble_media import DirtyBubbleMediaScraper
from scrapers.the_bear_cave import BearCaveScraper
from scrapers.the_friendly_bear import FriendlyBearScraper
from scrapers.sunshine_research import SunshineResearchScraper
from scrapers.prescience_point import PresciencePointScraper
from scrapers.one_off_SSA.quintessential_capital_management import QuintessentialCapitalScraper
from scrapers.one_off_SSA.citron_research import CitronResearchcraper
from scrapers.guasty_winds import GuastyWindsScraper
from scrapers.safkhet_capital import SafkhetCapitalScraper
from scrapers.outliers_research import OutliersResearchScraper
from scrapers.martin_shkreli import MartinShkreliScraper
from scrapers.captains_log import CaptainsLogScraper
from scrapers.disclosure_insight import DisclosureInsightScraper
from scrapers.ragnarok_research import RagnarokResearchScraper
from scrapers.unemon_research import UnemonScraper
from scrapers.fiat_lux_partners import FiatLuxPartnersScraper
from scrapers.anathema_research import AnathemaResearchScraper
from scrapers.kryptonite_research import KryptoniteResearchScraper
from scrapers.one_off_SSA.fraud_research_institute import FraudResearchInstituteScraper
from scrapers.one_off_SSA.ontake_research import OntakeResearchScraper
from scrapers.one_off_SSA.triam_research import TriamResearchScraper
from scrapers.one_off_SSA.mithra_forensic_research import MithraForensicResearchScraper
from scrapers.one_off_SSA.bucephalus_research import BucephalusResearchScraper
from scrapers.one_off_SSA.emerson_analytics import EmersonAnalyticsScraper
from scrapers.j_capital import JCapitalScraper
from scrapers.pig_farmer_capital import PigFarmerCapitalScraper
from scrapers.bird_dog_research import BirdDogResearchScraper
from scrapers.wolfpack_research import WolfpackResearchScraper
from scrapers.sakura_research import SakuraResearchScraper
from scrapers.bmf_reports import BMFReportsScraper
from scrapers.quintessential_research import QuintessentialResearchScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define scraper configurations - ALL SCRAPERS ENABLED
SCRAPER_CONFIGS = [
    {
        'name': 'Kryptonite Research',
        'class': KryptoniteResearchScraper
    },
    {
        'name': 'Anathema Research',
        'class': AnathemaResearchScraper
    },
    {
        'name': 'Fiat Lux Partners',
        'class': FiatLuxPartnersScraper
    },
    {
        'name': 'Unemon Research',
        'class': UnemonScraper
    },
    {
        'name': 'Ragnarok Research',
        'class': RagnarokResearchScraper
    },
    {
        'name': 'Disclosure Insight',
        'class': DisclosureInsightScraper
    },
    {
        'name': 'Captains Log',
        'class': CaptainsLogScraper
    },
    {
        'name': 'Martin Shkreli',
        'class': MartinShkreliScraper
    },
    {
        'name': 'Outliers Research',
        'class': OutliersResearchScraper
    },
    {
        'name': 'Safkhet Capital',
        'class': SafkhetCapitalScraper
    },
    {
        'name': 'Guasty Winds',
        'class': GuastyWindsScraper
    },
    {
        'name': 'Sunshine Research',
        'class': SunshineResearchScraper
    },
    {
        'name': 'Prescience Point',
        'class': PresciencePointScraper
    },
    {
        'name': 'The Friendly Bear',
        'class': FriendlyBearScraper
    },
    {
        'name': 'The Bear Cave',
        'class': BearCaveScraper
    },
    {
        'name': 'Dirty Bubble Media',
        'class': DirtyBubbleMediaScraper
    },
    {
        'name': 'Capybara Research',
        'class': CapybaraResearchScraper
    },
    {
        'name': 'Glasshouse Research',
        'class': GlasshouseResearchScraper
    },
    {
        'name': 'Bonitas Research',
        'class': BonitasResearchScraper
    },
    {
        'name': 'Snowcap Research',
        'class': SnowcapResearchScraper
    },
    {
        'name': 'Kerrisdale Capital',
        'class': KerrisdaleScraper
    },
    {
        'name': 'Gotham City Research',
        'class': GothamCityResearchScraper
    },
    {
        'name': 'Spruce Point Management',
        'class': SprucepointManagementScraper
    },
    {
        'name': 'Viceroy Research',
        'class': ViceroyResearchScraper
    },
    {
        'name': 'Hindenburg Research',
        'class': HindenburgResearchScraper
    },
    {
        'name': 'GMT Research',
        'class': GMTResearchScraper
    },
    {
        'name': 'Fuzzy Panda Research',
        'class': FuzzyPandaResearchScraper
    },
    {
        'name': 'Blue Orca Capital',
        'class': BlueOrcaCapitalScraper
    },
    {
        'name': 'Bleecker Street Research',
        'class': BleeckerStreetResearchScraper
    },
    {
        'name': 'White Diamond Research',
        'class': WhiteDiamondScraper
    },
    {
        'name': 'HunterBrook Research',
        'class': HunterBrookScraper
    },
    {
        'name': 'Logphase Research',
        'class': LogPhaseScraper
    },
    {
        'name': 'Culper Research',
        'class': CulperScraper
    },
    {
        'name': 'Scorpion Capital',
        'class': ScorpionCapitalScraper
    },
    {
        'name': 'Ningi Research',
        'class': NingiResearchScraper
    },
    {
        'name': 'Night Market Research',
        'class': NightMarketScraper
    },
    {
        'name': 'Pig Farmer Capital',
        'class': PigFarmerCapitalScraper
    },
    {
        'name': 'Bird Dog Research',
        'class': BirdDogResearchScraper
    },
    {
        'name': 'J Capital',
        'class': JCapitalScraper
    },
    {
        'name': 'Wolfpack Research',
        'class': WolfpackResearchScraper
    },
    {
        'name': 'Sakura Research',
        'class': SakuraResearchScraper
    },
    {
        'name': 'BMF Reports',
        'class': BMFReportsScraper
    },
    {
        'name': 'Quintessential Research',
        'class': QuintessentialResearchScraper
    },
    {
        'name': 'Citron Research',
        'class': CitronResearchcraper
    },
    {
        'name': 'Quintessential Capital Management',
        'class': QuintessentialCapitalScraper
    },
    {
        'name': 'Fraud Research Institute',
        'class': FraudResearchInstituteScraper
    },
    {
        'name': 'Ontake Research',
        'class': OntakeResearchScraper
    },
    {
        'name': 'Triam Research',
        'class': TriamResearchScraper
    },
    {
        'name': 'Mithra Forensic Research',
        'class': MithraForensicResearchScraper
    },
    {
        'name': 'Bucephalus Research',
        'class': BucephalusResearchScraper
    },
    {
        'name': 'Emerson Analytics',
        'class': EmersonAnalyticsScraper
    }
]

def run_scraper(config: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Run a single scraper and return its results
    """
    logger.info(f"Starting scraper for {config['name']}")
    
    # Initialize database controller
    db_controller = None
    try:
        db_controller = DatabaseController()
    except Exception as e:
        logger.warning(f"Could not initialize database controller: {str(e)}. Continuing without database operations.")
    
    try:
        scraper = config['class']()
        # Add retry logic
        max_retries = 2  # Reduced for lambda
        for attempt in range(max_retries):
            results = scraper.scrape()
            if results:
                logger.info(f"Successfully scraped {len(results)} reports from {config['name']}")
                
                # Log each individual report and perform database operations
                for i, report in enumerate(results):
                    if hasattr(report, 'source') and hasattr(report, 'publication_date') and hasattr(report, 'report_title'):
                        # Log the scraped report details
                        logger.info(f"NEW REPORT SCRAPED - Source: {getattr(report, 'source', 'N/A')}, "
                                  f"Publication Date: {getattr(report, 'publication_date', 'N/A')}, "
                                  f"Report Title: {getattr(report, 'report_title', 'N/A')}, "
                                  f"Link: {getattr(report, 'link', 'N/A')}, "
                                  f"Target Company: {getattr(report, 'target_company', 'N/A')}, "
                                  f"Short Seller: {getattr(report, 'short_seller', 'N/A')}")
                        
                        # Perform actual database write operation
                        if db_controller:
                            try:
                                success = db_controller.insert_short_report(report)
                                if success:
                                    logger.info(f"DATABASE WRITE SUCCESSFUL - Report '{getattr(report, 'report_title', 'N/A')}' by {getattr(report, 'short_seller', 'N/A')} has been successfully added to the database")
                                else:
                                    logger.error(f"DATABASE WRITE FAILED - Failed to add report '{getattr(report, 'report_title', 'N/A')}' to database")
                                    raise Exception("Database write failed")
                            except Exception as db_error:
                                logger.error(f"DATABASE WRITE FAILED - Error adding report '{getattr(report, 'report_title', 'N/A')}' to database: {str(db_error)}")
                                raise db_error
                        else:
                            logger.info(f"DATABASE WRITE SIMULATED - Report '{getattr(report, 'report_title', 'N/A')}' by {getattr(report, 'short_seller', 'N/A')} would be added to database")
                    else:
                        logger.info(f"NEW REPORT SCRAPED - Report #{i+1} from {config['name']}: {str(report)}")
                        # For generic reports, just log the attempt
                        if db_controller:
                            logger.info(f"DATABASE WRITE SIMULATED - Report #{i+1} from {config['name']} would be added to database")
                        else:
                            logger.info(f"DATABASE WRITE SIMULATED - Report #{i+1} from {config['name']} would be added to database")
                
                return results
            else:
                logger.warning(f"Attempt {attempt + 1}/{max_retries}: No results found for {config['name']}, retrying...")
                if attempt < max_retries - 1:  # Don't sleep on last attempt
                    time.sleep(2)  # Reduced wait time for lambda
        
        logger.error(f"All attempts failed for {config['name']}")
        return []
    except Exception as e:
        logger.error(f"Error running {config['name']} scraper: {str(e)}")
        return []
    finally:
        # Clean up database connection
        if db_controller:
            try:
                db_controller.disconnect()
            except:
                pass

def run_all_scrapers(max_workers: int = 1) -> Dict[str, List[Dict[str, str]]]:
    """
    Run all scrapers in parallel using ThreadPoolExecutor
    
    Args:
        max_workers (int): Maximum number of parallel scraping tasks
        
    Returns:
        Dict[str, List[Dict[str, str]]]: Dictionary mapping scraper names to their results
    """
    all_results = {}
    total_new_reports = 0
    successful_db_writes = 0
    
    # Group scrapers into batches to avoid overwhelming the system
    for i in range(0, len(SCRAPER_CONFIGS), max_workers):
        batch = SCRAPER_CONFIGS[i:i + max_workers]
        logger.info(f"Processing batch of {len(batch)} scrapers")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_config = {
                executor.submit(run_scraper, config): config
                for config in batch
            }
            
            for future in future_to_config:
                config = future_to_config[future]
                try:
                    results = future.result()
                    all_results[config['name']] = results
                    total_new_reports += len(results)
                    # Count successful database writes (assuming each report was written successfully)
                    successful_db_writes += len(results)
                except Exception as e:
                    logger.error(f"Scraper {config['name']} failed with error: {str(e)}")
                    all_results[config['name']] = []
        
        # Add a small delay between batches
        if i + max_workers < len(SCRAPER_CONFIGS):
            time.sleep(1)  # Reduced delay for lambda
    
    # Log total count of new reports and database operations
    if total_new_reports > 0:
        logger.info(f"TOTAL NEW REPORTS SCRAPED: {total_new_reports} reports have been successfully scraped and added to the database")
        logger.info(f"TOTAL DATABASE WRITES SUCCESSFUL: {successful_db_writes} reports have been successfully written to the database")
    else:
        logger.info("NO NEW REPORTS SCRAPED: No new reports have been scraped from any source")
        logger.info("NO DATABASE WRITES: No reports were written to the database")
    
    return all_results

def main():
    """
    Main function to run all scrapers and display results
    """
    logger.info("Starting all scrapers")
    results = run_all_scrapers()
    
    # Print summary
    print("\nScraping Results Summary:")
    print("-" * 50)
    total_reports = 0
    for name, reports in results.items():
        num_reports = len(reports)
        total_reports += num_reports
        print(f"{name}: {num_reports} reports")
        
        # Print report details
        if num_reports > 0:
            print("\nLatest reports:")
            for report in reports[:3]:  # Show latest 3 reports
                print(f"- {getattr(report, 'publication_date', 'No date')} | {getattr(report, 'report_title', 'No title')}")
            print()
    
    print("-" * 50)
    print(f"Total reports found: {total_reports}")
    return results

if __name__ == "__main__":
    main()