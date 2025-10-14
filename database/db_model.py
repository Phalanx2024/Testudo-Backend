import psycopg2
from psycopg2 import Error
import logging
from urllib.parse import urlparse

class DatabaseModel:
    def __init__(self, database_url):
        """
        Initialize database connection with Neon database URL
        Args:
            database_url (str): Complete Neon database URL
                format: postgres://user:password@host:port/database
        """
        self.database_url = database_url
        self.connection = None
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
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")

    def execute_query(self, query, params=None, fetch=False):
        """Base method to execute database queries"""
        try:
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                return result
            
            self.connection.commit()
            return True
            
        except Error as e:
            self.logger.error(f"Query execution error: {e}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
