import csv
import logging
import os

def save_reports_to_csv(reports, output_filename, destination_folder=None):
    """
    Save research reports to a CSV file.
    
    Args:
        reports: List of ResearchReport objects
        output_filename: Name of the output CSV file
        destination_folder: Optional custom destination folder path. 
                          If None, defaults to ~/Downloads/research_reports
    """
    if not reports:
        logging.warning("No reports to save")
        return
        
    try:
        # Use provided destination folder or default to ~/Downloads/research_reports
        output_dir = destination_folder or os.path.join(os.path.expanduser('~'), 'Downloads', 'research_reports')
        os.makedirs(output_dir, exist_ok=True)
        
        csv_path = os.path.join(output_dir, output_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'title', 'link', 'source'])
            writer.writeheader()
            writer.writerows([{
                'date': report.date,
                'title': report.title,
                'link': report.link,
                'source': report.source
            } for report in reports])
        logging.info(f"Data saved to {csv_path}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {str(e)}")