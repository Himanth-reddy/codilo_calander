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
    except Exception:
        return None

# --- Main Script ---
os.makedirs("public", exist_ok=True)
url = "https://node.codolio.com/api/contest-calendar/v1/all/get-upcoming-contests"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
    print(f"❌ Failed to fetch or parse API data. {e}")
    exit(1)

contest_list = data.get('data')

if not isinstance(contest_list, list):
    print("❌ Error: API 'data' key did not contain a list.")
    exit(1)

cal = Calendar()
cal.add('prodid', '-//Codolio Contests//mxm.dk//')
cal.add('version', '2.0')

for contest in contest_list:
    name = contest.get('contestName')
    start_time = safe_parse_date(contest.get('contestStartDate'))
    end_time = safe_parse_date(contest.get('contestEndDate'))
    url = contest.get('contestUrl', 'No link available')

    if not start_time or not end_time:
        continue  # Silently skip any contests with bad data

    event = Event()
    event.add('summary', name if name else 'Unnamed Contest')
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    event.add('description', url)
    cal.add_component(event)

ics_path = os.path.join("public", "codolio_contests.ics")
with open(ics_path, 'wb') as f:
    f.write(cal.to_ical())

print(f"✅ ICS file generated with {len(cal.subcomponents)} events.")
