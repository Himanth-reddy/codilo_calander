import os
import requests
from icalendar import Calendar, Event
from datetime import datetime
import pytz
import json

def safe_parse_date(date_str):
    """Safely parse ISO 8601 date strings into datetime objects."""
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        # Replace 'Z' with '+00:00' to make it ISO 8601 compatible
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone(pytz.UTC)
    except Exception as e:
        print(f"⚠️ Date parsing error for '{date_str}': {e}")
        return None

# Ensure public directory exists
os.makedirs("public", exist_ok=True)

# Codolio API endpoint
url = "https://node.codolio.com/api/contest-calendar/v1/all/get-upcoming-contests"

print("📡 Fetching data from Codolio API...")
response = requests.get(url)
data = response.json()

# Debug: Show JSON structure
print(json.dumps(data, indent=2))

# Find the list of contests in the JSON (now correctly targeting the 'data' key)
contest_list = data.get('data')

if contest_list is None:
    print("\n❌ No contest list found in the API response under the 'data' key.")
    exit(1)

# Create calendar
cal = Calendar()
cal.add('prodid', '-//Codolio Contests//mxm.dk//')
cal.add('version', '2.0')

# Add events
for contest in contest_list:
    event = Event()
    
    # --- UPDATED KEY NAMES ---
    event.add('summary', contest.get('contestName', 'Unnamed Contest'))
    start_time = safe_parse_date(contest.get('contestStartDate'))
    end_time = safe_parse_date(contest.get('contestEndDate'))
    description_url = contest.get('contestUrl', 'No link available')
    # -------------------------

    if not start_time or not end_time:
        print(f"⏭ Skipping '{contest.get('contestName')}' due to invalid date(s).")
        continue

    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('description', description_url)
    cal.add_component(event)

# Save to public folder
ics_path = os.path.join("public", "codolio_contests.ics")
with open(ics_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"\n✅ ICS file generated successfully: {ics_path}")
