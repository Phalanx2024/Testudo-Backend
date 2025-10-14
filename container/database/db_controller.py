import psycopg2
from psycopg2 import Error
import logging
from urllib.parse import urlparse
from database.db_model import DatabaseModel
from dotenv import load_dotenv
import os

class DatabaseController:
    def __init__(self):
        """Initialize database connection with Neon database URL from .env"""
        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL not found in .env file")
        self.db = DatabaseModel(database_url)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(self.database_url)
            if self.connection:
                self.logger.info("Successfully connected to Neon database")
                return True
        except Error as e:
            self.logger.error(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        self.db.disconnect()

    def insert_data(self, table_name, data_dict):
        """
        Insert data into specified table
        Args:
            table_name (str): Name of the table
            data_dict (dict): Dictionary containing column names and values
        """
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join([f'%s'] * len(data_dict))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        return self.db.execute_query(query, list(data_dict.values()))

    def bulk_insert(self, table_name, data_list):
        """
        Insert multiple rows of data
        Args:
            table_name (str): Name of the table
            data_list (list): List of dictionaries containing data to insert
        """
        if not data_list:
            return False
            
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join([f'%s'] * len(data_list[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        values_list = [tuple(item.values()) for item in data_list]
        
        return self.db.execute_query(query, values_list)

    def get_data(self, table_name, conditions=None):
        """
        Retrieve data from table
        Args:
            table_name (str): Name of the table
            conditions (dict): Optional filtering conditions
        """
        query = f"SELECT * FROM {table_name}"
        if conditions:
            where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
            return self.db.execute_query(query, list(conditions.values()), fetch=True)
        return self.db.execute_query(query, fetch=True)

    def get_link_from_short_sellers(self, short_seller_name):
        query = f"SELECT * FROM short_reports WHERE short_seller ='{short_seller_name}'"
        return self.db.execute_query(query, fetch=True)
    
    def insert_short_report(self, report):
        """
        Insert a single short report into the database
        Args:
            report: ResearchReport object
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert report to dictionary
            report_data = report.to_dict()
            
            # Insert with conflict handling (ON CONFLICT DO NOTHING)
            query = """
                INSERT INTO short_reports (publication_date, report_title, short_seller, last_update, link, target_company, ticker, sector)
                VALUES (%(publication_date)s, %(report_title)s, %(short_seller)s, NOW(), %(link)s, %(target_company)s, %(ticker)s, %(sector)s)
                ON CONFLICT DO NOTHING
            """
            
            # Add default values for missing fields
            report_data['sector'] = report_data.get('sector', '')
            report_data['last_update'] = 'NOW()'
            
            success = self.db.execute_query(query, report_data)
            if success:
                self.logger.info(f"Successfully added report to database: {report.report_title} by {report.short_seller}")
                return True
            else:
                self.logger.error(f"Failed to add report to database: {report.report_title} by {report.short_seller}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error inserting report {report.report_title}: {str(e)}")
            return False

# Example usage:
if __name__ == "__main__":

    db = DatabaseController()
    # Example single insert
    sample_data = {
        "month": "Joh",
        "revenue": 0
    }
    db.insert_data("revenue", sample_data)
    
    # Example bulk insert
    # bulk_data = [
    #     {"name": "Jane Doe", "email": "jane@example.com", "age": 25},
    #     {"name": "Bob Smith", "email": "bob@example.com", "age": 35}
    # ]
    # db.bulk_insert("revenue", bulk_data)
    
    # Close the connection
    db.disconnect() 