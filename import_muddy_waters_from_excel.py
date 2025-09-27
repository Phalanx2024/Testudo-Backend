import os
import sys
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
from dotenv import load_dotenv

from database.db_controller import DatabaseController
import re


def load_excel(filepath: str):
    df = pd.read_excel(filepath, sheet_name='Muddy Waters', engine='openpyxl', header=None)
    # Find header row dynamically by searching for expected column names
    expected_markers = {'date', 'company', 'ticker', 'sector'}
    header_row = None
    search_limit = min(len(df), 100)
    for i in range(search_limit):
        row_values = set(str(v).strip().lower() for v in df.iloc[i].tolist())
        if expected_markers.issubset(row_values):
            header_row = i
            break
    # Fallback to row 24 (index 24) if not found
    if header_row is None:
        # Excel data starts at row 25 => header likely at row 24; pandas index is 0-based -> 23
        header_row = 23
    # Set header
    headers = [str(c).strip() for c in df.iloc[header_row].tolist()]
    df = df.iloc[header_row + 1 :].copy()
    df.columns = headers
    # Normalize duplicate/empty column names
    df.columns = [c if c else f"Unnamed_{i}" for i, c in enumerate(df.columns)]
    return df, header_row


def map_row_to_record(row: pd.Series, colmap: dict) -> dict:
    pub_date_raw = row.get('Date')
    publication_date = None
    if pd.notna(pub_date_raw):
        if isinstance(pub_date_raw, (datetime, pd.Timestamp)):
            publication_date = pub_date_raw.date()
        else:
            try:
                publication_date = pd.to_datetime(str(pub_date_raw)).date()
            except Exception:
                publication_date = None

    target_company = row.get(colmap['Company']) if pd.notna(row.get(colmap['Company'])) else ''
    ticker = row.get(colmap['Ticker']) if pd.notna(row.get(colmap['Ticker'])) else ''
    sector = row.get(colmap['Sector']) if pd.notna(row.get(colmap['Sector'])) else ''
    link = row.get(colmap['Link']) if pd.notna(row.get(colmap['Link'])) else ''

    # Build a unique-ish title using company and date
    title_parts = [target_company.strip()] if target_company else []
    if publication_date:
        title_parts.append(publication_date.isoformat())
    report_title = ' - '.join(title_parts) if title_parts else target_company or link

    return {
        'publication_date': publication_date,
        'report_title': report_title,
        'link': link,
        'target_company': target_company,
        'short_seller': 'Muddy Waters Research',
        'ticker': ticker,
        'sector': sector,
        'last_update': datetime.utcnow().date(),
    }


def fetch_existing_links(db: DatabaseController) -> set:
    try:
        result = db.db.execute_query("SELECT link FROM short_reports WHERE short_seller = 'Muddy Waters Research'", fetch=True)
        if result:
            return set(r[0] for r in result if r and r[0])
    except Exception:
        pass
    return set()


def fetch_existing_titles(db: DatabaseController) -> set:
    try:
        result = db.db.execute_query("SELECT report_title FROM short_reports WHERE short_seller = 'Muddy Waters Research'", fetch=True)
        if result:
            return set(r[0] for r in result if r and r[0])
    except Exception:
        pass
    return set()


def insert_records(db: DatabaseController, records: list) -> int:
    inserted = 0
    for rec in records:
        if db.insert_data('short_reports', rec):
            inserted += 1
    return inserted


def main():
    if len(sys.argv) < 2:
        print('Usage: python import_muddy_waters_from_excel.py "/path/to/SSA Report Database.xlsx"')
        sys.exit(1)

    excel_path = sys.argv[1]
    if not os.path.isfile(excel_path):
        print(f'File not found: {excel_path}')
        sys.exit(1)

    load_dotenv()
    df, header_row = load_excel(excel_path)
    # Build a flexible column map
    lower_cols = {c.lower().strip(): c for c in df.columns}
    def first_match(options):
        for opt in options:
            if opt in lower_cols:
                return lower_cols[opt]
        return None

    colmap = {
        'Date': first_match(['date']),
        'Company': first_match(['company']),
        'Ticker': first_match(['ticker']),
        'Sector': first_match(['sector']),
        'Link': first_match(['link', 'links', 'url', 'report link', 'report url', 'source', 'website'])
    }

    missing = [k for k, v in colmap.items() if v is None and k in ['Date','Company','Link']]
    if missing:
        print(f"Missing required columns in sheet Muddy Waters: {', '.join(missing)}")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)

    # Keep only rows with some link-ish content
    df = df[df.get(colmap['Link']).notna()]

    # Try to extract real hyperlink targets from the worksheet for the Link column
    wb = load_workbook(excel_path, data_only=True, read_only=True)
    ws = wb['Muddy Waters']
    link_col_idx = df.columns.get_loc(colmap['Link'])  # 0-based

    records = []
    for i, (_, row) in enumerate(df.iterrows()):
        rec = map_row_to_record(row, colmap)
        # Compute sheet row number (1-based): header_row is 0-based pandas index, add 2 for header+1, plus i offset
        sheet_row_num = header_row + 2 + i
        cell = ws.cell(row=sheet_row_num, column=link_col_idx + 1)
        link_target = None
        if cell is not None and getattr(cell, 'hyperlink', None) is not None:
            link_target = getattr(cell.hyperlink, 'target', None)
        # Prefer hyperlink target if it looks like a URL
        val = str(rec.get('link') or '').strip()
        def extract_url(s: str) -> str:
            if not s:
                return ''
            # If starts with scheme
            if s.lower().startswith(('http://','https://')):
                return s
            # Find any http(s) substring in text
            m = re.search(r'(https?://[^\s\)\]]+)', s, flags=re.IGNORECASE)
            if m:
                return m.group(1)
            # Handle www. without scheme
            m2 = re.search(r'(www\.[^\s\)\]]+)', s, flags=re.IGNORECASE)
            if m2:
                return 'https://' + m2.group(1)
            return ''

        if link_target and str(link_target).lower().startswith(('http://','https://')):
            rec['link'] = str(link_target)
        else:
            # Try cell text
            cell_text = str(cell.value) if cell and cell.value is not None else ''
            url = extract_url(cell_text) or extract_url(val)
            if url:
                rec['link'] = url
        records.append(rec)

    # Intra-batch dedupe by link
    seen = set()
    unique_records = []
    for rec in records:
        link = rec['link']
        if not link or link in seen:
            continue
        seen.add(link)
        unique_records.append(rec)

    db = DatabaseController()
    existing_links = fetch_existing_links(db)
    existing_titles = fetch_existing_titles(db)
    to_insert = [r for r in unique_records if r['link'] not in existing_links and r['report_title'] not in existing_titles]

    inserted = insert_records(db, to_insert)
    print(f'Prepared {len(records)} records, {len(unique_records)} unique by link, {len(to_insert)} new. Inserted: {inserted}.')


if __name__ == '__main__':
    main()


