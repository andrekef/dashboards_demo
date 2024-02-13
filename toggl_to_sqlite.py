import requests
import sqlite3
from datetime import datetime, timedelta

# Define your Toggl API token
api_token = 'yourApiToken'

# Define page size and initial start date
page_size = 1000
start_date = '2023-01-01T00:00:00Z'
end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# Make initial request to get total count
initial_url = f'https://api.track.toggl.com/api/v8/time_entries?start_date={start_date}&end_date={end_date}'
initial_response = requests.get(initial_url, auth=(api_token, 'api_token'))

if initial_response.status_code == 200:
    total_entries = initial_response.headers.get('X-Total-Count', 0)
    print(f"Total entries: {total_entries}")
    
    # Calculate number of pages
    total_pages = (int(total_entries) + page_size - 1) // page_size
    
    # Store data in SQLite database
    conn = sqlite3.connect('pivotal_data.db')
    cursor = conn.cursor()

    # Create a table for time entries if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_entries (
            id TEXT PRIMARY KEY,
            wid INTEGER,
            pid INTEGER,
            tid INTEGER,
            billable INTEGER,
            start TEXT,
            stop TEXT,
            duration INTEGER,
            description TEXT,
            duronly INTEGER,
            at TEXT,
            uid INTEGER
        )
    ''')

    # Clear existing data in the 'time_entries' table
    cursor.execute("DELETE FROM time_entries")

    # Paginate through the data
    for page in range(total_pages):
        offset = page * page_size
        url = f'https://api.track.toggl.com/api/v9/me/time_entries?start_date={start_date}&end_date={end_date}&offset={offset}&limit={page_size}'
        response = requests.get(url, auth=(api_token, 'api_token'))
        
        if response.status_code == 200:
            time_entries = response.json()
            
            # Insert time entries into the table
            for entry in time_entries:
                cursor.execute('''
                    INSERT INTO time_entries 
                    (id, wid, pid, tid, billable, start, stop, duration, description, duronly, at, uid) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry['id'], entry.get('wid', 0), entry.get('pid', 0), entry.get('tid', 0),
                    entry.get('billable', 0), entry.get('start', ''), entry.get('stop', ''),
                    entry.get('duration', 0), entry.get('description', ''), entry.get('duronly', 0),
                    entry.get('at', ''), entry.get('uid', 0)
                ))
            
            # Commit changes after each page to reduce potential data loss
            conn.commit()
        else:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
    
    # Close connection
    conn.close()

    print("Time entries saved to SQLite database.")
else:
    print(f"Failed to retrieve initial data. Status code: {initial_response.status_code}")
