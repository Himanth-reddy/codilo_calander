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
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone(pytz.UTC)
    except Exception as e:
        print(f"⚠️  Date parsing error for '{date_str}': {e}")
        return None

# --- Main Script ---
os.makedirs("public", exist_ok=True)
url = "https://node.codolio.com/api/contest-calendar/v1/all/get-upcoming-contests"

print("📡 Fetching data from Codolio API...")
try:
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error for bad status codes (4xx or 5xx)
    data = response.json()
except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
    print(f"❌ Critical Error: Failed to fetch or parse API data. {e}")
    exit(1)

contest_list = data.get('data')

# More robust check
if not isinstance(contest_list, list):
    print(f"❌ Error: The API response's 'data' key did not contain a list. Found: {type(contest_list)}")
    exit(1)

if not contest_list:
    print("✅ API returned an empty list of contests. Nothing to do.")
else:
    print(f"✅ Found {len(contest_list)} contests in the API response.")

cal = Calendar()
cal.add('prodid', '-//Codolio Contests//mxm.dk//')
cal.add('version', '2.0')

for i, contest in enumerate(contest_list):
    print(f"\n--- Processing contest {i+1} ---")

    # Get values from the contest dictionary
    name = contest.get('contestName')
    start_str = contest.get('contestStartDate')
    end_str = contest.get('contestEndDate')
    url = contest.get('contestUrl', 'No link available')

    print(f"  - Read Name: {name}")
    print(f"  - Read Start String: {start_str}")
    print(f"  - Read End String: {end_str}")

    # Parse dates
    start_time = safe_parse_date(start_str)
    end_time = safe_parse_date(end_str)

    print(f"  - Parsed Start Time: {start_time}")
    print(f"  - Parsed End Time: {end_time}")

    if not start_time or not end_time:
        print(f"  - 🔴 SKIPPING: Invalid or missing date(s).")
        continue

    event = Event()
    event.add('summary', name if name else 'Unnamed Contest')
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('description', url)
    cal.add_component(event)
    print(f"  - 🟢 ADDED to calendar.")


ics_path = os.path.join("public", "codolio_contests.ics")
with open(ics_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"\n✅ ICS file generated successfully with {len(cal.subcomponents)} events.")
