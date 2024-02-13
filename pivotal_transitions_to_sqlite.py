import requests
import sqlite3
import json

# Replace with your Pivotal Tracker API token
PIVOTAL_TOKEN = 'yourApiToken'

# API endpoint for story_transitions
api_url_transitions = 'https://www.pivotaltracker.com/services/v5/projects/1198900/story_transitions'

# Set up headers with Pivotal Tracker API token
headers = {'X-TrackerToken': PIVOTAL_TOKEN}

# Initialize variables for pagination
offset = 0
limit = 10000
all_data_transitions = []

while True:
    # Make API request with pagination parameters
    params = {'limit': limit, 'offset': offset}
    response = requests.get(api_url_transitions, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data_transitions = response.json()

        # If there are no more records, break the loop
        if not data_transitions:
            break

        # Append the current batch of data to the overall data list
        all_data_transitions.extend(data_transitions)

        # Increment the offset for the next batch
        offset += limit
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        break

# Print or process the combined data
print(json.dumps(all_data_transitions, indent=2))

# Store data in SQLite database
conn = sqlite3.connect('pivotal_data.db')
cursor = conn.cursor()

# Create a new table 'story_transitions' (Assuming it has not been created yet)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS story_transitions (
        kind TEXT,
        story_id INTEGER,
        state TEXT,
        project_id INTEGER,
        project_version INTEGER,
        occurred_at TEXT,
        performed_by_id INTEGER
    )
''')

# Insert data into the 'story_transitions' table
for transition in all_data_transitions:
    cursor.execute("""
        INSERT OR IGNORE INTO story_transitions
        (kind, story_id, state, project_id, project_version, occurred_at, performed_by_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        transition.get('kind', ''), transition.get('story_id', 0), transition.get('state', ''),
        transition.get('project_id', 0), transition.get('project_version', 0),
        transition.get('occurred_at', ''), transition.get('performed_by_id', 0)
    ))

conn.commit()
conn.close()
