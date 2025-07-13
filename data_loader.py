import psycopg2
import pandas as pd
from datetime import datetime, date
from typing import List, Dict, Optional
import json
from dotenv import load_dotenv
import os

load_dotenv()

class ResearchReportDataLoader:
    """Data loader for research reports from database"""
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'testudo'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'port': os.getenv('DB_PORT', '5432')
        }
    
    def get_connection(self):
        """Get database connection"""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def load_reports_from_database(self, limit: Optional[int] = None) -> List[Dict]:
        """Load research reports from database"""
        connection = self.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            
            # Query to get reports with all necessary fields
            query = """
                SELECT 
                    publication_date,
                    report_title,
                    link,
                    target_company,
                    short_seller,
                    ticker,
                    sector,
                    last_update
                FROM short_reports
                ORDER BY publication_date DESC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            reports = []
            for row in rows:
                report = {
                    'publication_date': row[0],
                    'report_title': row[1],
                    'link': row[2],
                    'target_company': row[3],
                    'short_seller': row[4],
                    'ticker': row[5] if row[5] else '',
                    'sector': row[6] if row[6] else '',
                    'last_update': row[7],
                    'source': 'database',
                    'report_text': ''  # Will be populated later if needed
                }
                reports.append(report)
            
            cursor.close()
            connection.close()
            
            print(f"Loaded {len(reports)} reports from database")
            return reports
            
        except Exception as e:
            print(f"Error loading reports: {e}")
            if connection:
                connection.close()
            return []
    
    def load_reports_with_text(self, limit: Optional[int] = None) -> List[Dict]:
        """Load reports and attempt to get full text content"""
        reports = self.load_reports_from_database(limit)
        
        # For now, we'll use the report title as a proxy for text content
        # In a real implementation, you'd want to scrape the full text from the links
        for report in reports:
            report['report_text'] = report['report_title']  # Placeholder
        
        return reports
    
    def get_reports_by_company(self, company_name: str) -> List[Dict]:
        """Get all reports for a specific company"""
        connection = self.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            
            query = """
                SELECT 
                    publication_date,
                    report_title,
                    link,
                    target_company,
                    short_seller,
                    ticker,
                    sector,
                    last_update
                FROM short_reports
                WHERE LOWER(target_company) LIKE LOWER(%s)
                ORDER BY publication_date DESC
            """
            
            cursor.execute(query, (f'%{company_name}%',))
            rows = cursor.fetchall()
            
            reports = []
            for row in rows:
                report = {
                    'publication_date': row[0],
                    'report_title': row[1],
                    'link': row[2],
                    'target_company': row[3],
                    'short_seller': row[4],
                    'ticker': row[5] if row[5] else '',
                    'sector': row[6] if row[6] else '',
                    'last_update': row[7],
                    'source': 'database',
                    'report_text': row[1]  # Using title as placeholder
                }
                reports.append(report)
            
            cursor.close()
            connection.close()
            
            print(f"Loaded {len(reports)} reports for company: {company_name}")
            return reports
            
        except Exception as e:
            print(f"Error loading company reports: {e}")
            if connection:
                connection.close()
            return []
    
    def get_reports_by_firm(self, firm_name: str) -> List[Dict]:
        """Get all reports from a specific research firm"""
        connection = self.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            
            query = """
                SELECT 
                    publication_date,
                    report_title,
                    link,
                    target_company,
                    short_seller,
                    ticker,
                    sector,
                    last_update
                FROM short_reports
                WHERE LOWER(short_seller) LIKE LOWER(%s)
                ORDER BY publication_date DESC
            """
            
            cursor.execute(query, (f'%{firm_name}%',))
            rows = cursor.fetchall()
            
            reports = []
            for row in rows:
                report = {
                    'publication_date': row[0],
                    'report_title': row[1],
                    'link': row[2],
                    'target_company': row[3],
                    'short_seller': row[4],
                    'ticker': row[5] if row[5] else '',
                    'sector': row[6] if row[6] else '',
                    'last_update': row[7],
                    'source': 'database',
                    'report_text': row[1]  # Using title as placeholder
                }
                reports.append(report)
            
            cursor.close()
            connection.close()
            
            print(f"Loaded {len(reports)} reports from firm: {firm_name}")
            return reports
            
        except Exception as e:
            print(f"Error loading firm reports: {e}")
            if connection:
                connection.close()
            return []
    
    def get_reports_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """Get reports within a specific date range"""
        connection = self.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor()
            
            query = """
                SELECT 
                    publication_date,
                    report_title,
                    link,
                    target_company,
                    short_seller,
                    ticker,
                    sector,
                    last_update
                FROM short_reports
                WHERE publication_date BETWEEN %s AND %s
                ORDER BY publication_date DESC
            """
            
            cursor.execute(query, (start_date, end_date))
            rows = cursor.fetchall()
            
            reports = []
            for row in rows:
                report = {
                    'publication_date': row[0],
                    'report_title': row[1],
                    'link': row[2],
                    'target_company': row[3],
                    'short_seller': row[4],
                    'ticker': row[5] if row[5] else '',
                    'sector': row[6] if row[6] else '',
                    'last_update': row[7],
                    'source': 'database',
                    'report_text': row[1]  # Using title as placeholder
                }
                reports.append(report)
            
            cursor.close()
            connection.close()
            
            print(f"Loaded {len(reports)} reports from {start_date} to {end_date}")
            return reports
            
        except Exception as e:
            print(f"Error loading date range reports: {e}")
            if connection:
                connection.close()
            return []
    
    def get_database_statistics(self) -> Dict:
        """Get database statistics"""
        connection = self.get_connection()
        if not connection:
            return {}
        
        try:
            cursor = connection.cursor()
            
            # Total reports
            cursor.execute("SELECT COUNT(*) FROM short_reports")
            total_reports = cursor.fetchone()[0]
            
            # Unique companies
            cursor.execute("SELECT COUNT(DISTINCT target_company) FROM short_reports")
            unique_companies = cursor.fetchone()[0]
            
            # Unique firms
            cursor.execute("SELECT COUNT(DISTINCT short_seller) FROM short_reports")
            unique_firms = cursor.fetchone()[0]
            
            # Date range
            cursor.execute("SELECT MIN(publication_date), MAX(publication_date) FROM short_reports")
            date_range = cursor.fetchone()
            
            # Top companies by report count
            cursor.execute("""
                SELECT target_company, COUNT(*) as report_count 
                FROM short_reports 
                GROUP BY target_company 
                ORDER BY report_count DESC 
                LIMIT 10
            """)
            top_companies = cursor.fetchall()
            
            # Top firms by report count
            cursor.execute("""
                SELECT short_seller, COUNT(*) as report_count 
                FROM short_reports 
                GROUP BY short_seller 
                ORDER BY report_count DESC 
                LIMIT 10
            """)
            top_firms = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            stats = {
                'total_reports': total_reports,
                'unique_companies': unique_companies,
                'unique_firms': unique_firms,
                'date_range': {
                    'earliest': date_range[0].isoformat() if date_range[0] else None,
                    'latest': date_range[1].isoformat() if date_range[1] else None
                },
                'top_companies': [{'company': row[0], 'count': row[1]} for row in top_companies],
                'top_firms': [{'firm': row[0], 'count': row[1]} for row in top_firms]
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting database statistics: {e}")
            if connection:
                connection.close()
            return {}
    
    def export_to_csv(self, filename: str = 'research_reports.csv', limit: Optional[int] = None):
        """Export reports to CSV file"""
        reports = self.load_reports_from_database(limit)
        
        if reports:
            df = pd.DataFrame(reports)
            df.to_csv(filename, index=False)
            print(f"Exported {len(reports)} reports to {filename}")
        else:
            print("No reports to export")
    
    def export_to_json(self, filename: str = 'research_reports.json', limit: Optional[int] = None):
        """Export reports to JSON file"""
        reports = self.load_reports_from_database(limit)
        
        if reports:
            # Convert dates to strings for JSON serialization
            for report in reports:
                if report['publication_date']:
                    report['publication_date'] = report['publication_date'].isoformat()
                if report['last_update']:
                    report['last_update'] = report['last_update'].isoformat()
            
            with open(filename, 'w') as f:
                json.dump(reports, f, indent=2)
            
            print(f"Exported {len(reports)} reports to {filename}")
        else:
            print("No reports to export")

# Example usage
if __name__ == "__main__":
    loader = ResearchReportDataLoader()
    
    # Get database statistics
    stats = loader.get_database_statistics()
    print("Database Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Load sample reports
    sample_reports = loader.load_reports_from_database(limit=100)
    print(f"\nLoaded {len(sample_reports)} sample reports")
    
    # Export to files
    loader.export_to_csv('sample_reports.csv', limit=100)
    loader.export_to_json('sample_reports.json', limit=100) 