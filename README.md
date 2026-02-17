# Codolio Contest Calendar

A simple project that fetches upcoming coding contests from the Codolio API and provides:

- A web calendar view (`index.html`) powered by FullCalendar.
- Platform-specific `.ics` feeds users can subscribe to in Google Calendar.
- Automated feed refresh every 6 hours via GitHub Actions + GitHub Pages deployment.

## How automated updates work

1. The workflow in `.github/workflows/update.yml` runs every 6 hours (`0 */6 * * *` UTC) and also on pushes to `main`.
2. It runs `python codolio_to_calendar.py` to regenerate `public/*.ics`.
3. It deploys `public/` to GitHub Pages.
4. Users subscribe once in Google Calendar using the hosted `.ics` URL, and Google refreshes events periodically.

## Files

- `index.html` - Frontend calendar UI and subscription links.
- `codolio_to_calendar.py` - Script that fetches contests and generates `.ics` files in `public/`.
- `public/*.ics` - Generated iCalendar feed files.
- `.github/workflows/update.yml` - Scheduled automation + deploy workflow.

## Generate `.ics` feeds locally

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

## Subscribe in Google Calendar

Use the hosted feed URL format:

```text
https://himanth-reddy.github.io/codilo_calander/leetcode_contests.ics
```

In Google Calendar:

1. Open **Other calendars** -> **+** -> **From URL**
2. Paste the feed URL
3. Click **Add calendar**

Google updates subscribed calendars automatically, but refresh timing is controlled by Google and is not instant.

## Serve locally (preview)

```bash
python3 -m http.server 8000
```

Then open:

- `http://localhost:8000/index.html`

## Data source

- `https://node.codolio.com/api/contest-calendar/v1/all/get-upcoming-contests`
