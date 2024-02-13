import requests
import sqlite3
import json
from datetime import datetime

# Replace with your Pivotal Tracker API token
PIVOTAL_TOKEN = 'yourApiToken'

# API endpoint
api_url = 'https://www.pivotaltracker.com/services/v5/projects/1198900/stories'

# Set up headers with Pivotal Tracker API token
headers = {'X-TrackerToken': PIVOTAL_TOKEN}

# Define the time range (from January 1, 2023, to December 31, 2024)
start_date = datetime(2023, 1, 1).isoformat() + 'Z'
end_date = datetime(2024, 12, 31).isoformat() + 'Z'

# Initialize variables for pagination
offset = 0
limit = 10000
all_data = []

while True:
    # Make API request with pagination parameters and time range filter
    params = {'limit': limit, 'offset': offset, 'filter': f'created_since:{start_date} created_before:{end_date}'}
    response = requests.get(api_url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # If there are no more records, break the loop
        if not data:
            break

        # Append the current batch of data to the overall data list
        all_data.extend(data)

        # Increment the offset for the next batch
        offset += limit
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        break

# Print or process the combined data
print(json.dumps(all_data, indent=2))

# Store data in SQLite database
conn = sqlite3.connect('pivotal_data.db')
cursor = conn.cursor()

# Clear existing data in the 'stories' table
cursor.execute("DELETE FROM stories")

# Assume 'stories' table is already created
for story in all_data:
    cursor.execute("""
        INSERT OR IGNORE INTO stories 
        (kind, id, created_at, updated_at, story_type, story_priority, name, description, current_state, requested_by_id, url, project_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        story.get('kind', ''), story.get('id', 0), story.get('created_at', ''), story.get('updated_at', ''), 
        story.get('story_type', ''), story.get('story_priority', ''), story.get('name', ''), 
        story.get('description', ''), story.get('current_state', ''), story.get('requested_by_id', 0), 
        story.get('url', ''), story.get('project_id', 0)
    ))

conn.commit()
conn.close()

# Print the update timestamp
print(f'Data updated at: {datetime.now()}')