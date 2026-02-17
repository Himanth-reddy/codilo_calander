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

On the hosted website (`https://himanth-reddy.github.io/codilo_calander/`), each subscription button now opens Google Calendar’s subscribe flow directly.

- Click a button like **Add LeetCode to Google Calendar**.
- A new tab opens to Google Calendar with the feed URL pre-filled.
- Confirm the subscription in Google Calendar.

If you need the raw feed URL format, it is:

```text
https://himanth-reddy.github.io/codilo_calander/leetcode_contests.ics
```

## Serve locally (for preview)

```bash
python3 -m http.server 8000
```

Then open:

- `http://localhost:8000/index.html`

## Data source

Contests are fetched from:

- `https://node.codolio.com/api/contest-calendar/v1/all/get-upcoming-contests`
