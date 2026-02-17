# Codolio Contest Calendar

A simple project that fetches upcoming coding contests from the Codolio API and provides:

- A web calendar view (`index.html`) powered by FullCalendar.
- Platform-specific `.ics` feeds you can subscribe to in calendar clients (including Google Calendar).

## Files

- `index.html` – Frontend calendar UI and subscription links.
- `codolio_to_calendar.py` – Script that fetches contests and generates `.ics` files in `public/`.
- `public/*.ics` – Generated iCalendar feed files (created after running the Python script).

## Generate `.ics` feeds

1. Install dependencies:

```bash
python3 -m pip install requests icalendar pytz
```

2. Run the generator:

```bash
python3 codolio_to_calendar.py
```

This creates:

- `public/leetcode_contests.ics`
- `public/atcoder_contests.ics`
- `public/codeforces_contests.ics`
- `public/codechef_contests.ics`
- `public/geeksforgeeks_contests.ics`

## Use with Google Calendar

Google Calendar subscription requires a **public, absolute URL** to an `.ics` file.

Example format:

```text
https://your-domain.com/leetcode_contests.ics
```

In Google Calendar:

1. Open **Other calendars** → **+** → **From URL**.
2. Paste the full URL to your `.ics` feed.
3. Click **Add calendar**.

> Note: Local file paths or relative links (like `./leetcode_contests.ics`) will not work in Google Calendar's “From URL” subscription.

## Serve locally (for preview)

```bash
python3 -m http.server 8000
```

Then open:

- `http://localhost:8000/index.html`

## Data source

Contests are fetched from:

- `https://node.codolio.com/api/contest-calendar/v1/all/get-upcoming-contests`
