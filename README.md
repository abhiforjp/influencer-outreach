# Automated Micro-Influencer Outreach System
**Assignment 4 — finding Indian micro-influencers, enriching their profiles, and reaching out with personalized messages**

This project finds Indian micro-influencers (5,000–100,000 followers), builds a
clean dataset around them, writes each one a personalized collaboration pitch,
and ships a Gmail/SMTP sending layer that won't send anything by accident. It
runs under a demo brand called **UrbanNest** — swap in a real brand by editing
`src/config.py`.

## The numbers
- **53 Indian micro-influencers** across 5 niches: Tech (13), Travel (11), Food (11), Lifestyle (10), Fitness (8)
- **Every single profile was checked by hand** — the original research found 64, but 11 turned out to have dead or broken Instagram/YouTube links, so they were cut. Follower counts were also refreshed to live numbers during the same check (July 2026).
- **43 of 53 (81%) have a working, publicly listed contact email**, and the sheet records exactly where each email was found. The other 10 are marked DM-only — no emails were guessed or made up.
- **1 filtered segment**: Lifestyle & Travel creators with a verified email and at least 2% engagement (16 creators)
- **53 personalized emails (60–90 words) and 53 Instagram DMs (15–30 words)** — the word limits are enforced by the code itself, so an out-of-range message can't be generated
- **An EDA notebook** (`influencer_eda.ipynb`) with 9 visualizations digging into the dataset

## What's in the folder
```
influencer-outreach/
├── data/influencers_raw.csv          # the hand-verified dataset (53 rows)
├── influencer_eda.ipynb              # exploratory analysis, charts embedded
├── src/
│   ├── config.py                     # brand, niche playbook, benchmarks, SMTP
│   ├── discovery.py                  # step 1: finding creators in directories
│   ├── enrichment.py                 # steps 2-3: validation, ER fill, fit score
│   ├── filters.py                    # step 2: segments
│   ├── personalize.py                # step 4: email + DM generation
│   ├── send_emails.py                # step 5: Gmail sender (dry-run by default)
│   ├── export_excel.py               # builds the Excel deliverable
│   └── main.py                       # runs the whole pipeline
├── output/                           # everything the pipeline produces
│   ├── influencers_enriched.csv
│   ├── segment_lifestyle_travel.csv
│   ├── outreach_messages.csv
│   ├── email_templates.md
│   ├── instagram_dm_templates.md
│   └── indian_micro_influencers.xlsx # 4-sheet Excel deliverable
└── requirements.txt
```

## How it works

### 1. Finding the creators
The list was built from public creator directories — Feedspot's niche and city
lists (Indian Lifestyle, Travel, Food, Fitness, Yoga, Tech YouTube, plus city
pages like Kolkata and Jaipur) and StarNgage's free India rankings, which also
report engagement rates — along with hashtag searches (#IndianTravel, #FitIndia,
#IndianFoodBlogger and so on) and the creators' own blogs and channels.
`src/discovery.py` automates the directory scraping part and filters candidates
to the 5k–100k band. Directories go stale though, which is exactly why the
manual re-check mattered: 11 of the 64 originally listed accounts no longer
worked and were dropped.

### 2. Filtering
`src/filters.py` slices the dataset by niche, email availability, and
engagement rate. The segment included here — Lifestyle + Travel creators with a
verified email and ER ≥ 2% — is the natural first outreach list for a
home-and-travel brand like UrbanNest.

### 3. Enriching the profiles
`src/enrichment.py` fills out each row: platforms, live follower count,
engagement rate, niche, content themes, contact email plus its source, profile
link, city, and a 0–100 brand-fit score used to rank the outreach order. On
engagement rates, honesty matters: only 4 creators have directory-measured ERs,
and the rest use India micro-tier benchmarks that are clearly labelled
"estimated" in the sheet. Nobody should mistake a benchmark for a measurement.

### 4. Writing the messages
`src/personalize.py` builds every message from the creator's niche (which maps
to a collaboration type, product line, and offer through the `NICHE_PLAYBOOK`
in config), their content themes, city, platform, and handle. So a food
creator gets offered a sponsored tasting with a product hamper, while a tech
creator gets a paid review with affiliate commission. The assignment's word
limits (60–90 for emails, 15–30 for DMs) are baked in as assertions — if a
message ever falls outside the range, the build fails instead of shipping it.

### 5. Sending
`src/send_emails.py` uses Gmail SMTP over SSL and is dry-run by default —
nothing is actually sent without the `--send` flag.

```bash
python src/send_emails.py                                    # just a preview
export SMTP_USER="user@gmail.com" SMTP_PASS="app-password"   # Gmail App Password
python src/send_emails.py --send --test-to user@gmail.com --limit 3   # safe demo
python src/send_emails.py --send                             # the real thing
```

Instagram DMs are left un-automated on purpose — bot DMs violate Instagram's
terms. The DM copy is exported ready to paste, and at scale it could go
through an official Meta messaging partner instead.

## The EDA notebook
`influencer_eda.ipynb` cleans the data, engineers a few features (primary
platform, email flag, reported-vs-estimated ER, city, follower bands), and
then makes its case in 9 charts: a niche × follower-band heatmap, a violin +
swarm plot where every creator is a dot colored by reachability, a bubble
chart of followers vs engagement sized by brand fit, a reachability funnel per
niche, the measured ERs plotted against the benchmark lines, a radar
comparison of the five niches, a top-15 lollipop ranking, a city × niche
heatmap, and a word-count compliance check on all the generated messages.

The short version of the findings: reachability is structural — creators who
own a blog or YouTube channel publish contact emails (Travel and Tech are 100%
reachable), while bio-only Instagram creators mostly don't (Lifestyle is 50%).
Measured engagement varies about 6× between accounts of the same size, so
benchmarks are placeholders at best. And the standout target is
@caffeinatedmomblogger — roughly 100K followers with a measured 6.34%
engagement rate and a verified email.

## Running it
```bash
pip install -r requirements.txt
python src/main.py            # enrich -> segment -> personalize -> dry-run preview
python src/export_excel.py    # rebuild the Excel file
python src/discovery.py       # optional: re-scrape directory candidates
```

## A few honest caveats
- All the data comes from public sources — directories, public bios, About pages, and the creators' own sites. It was collected and hand-verified in July 2026, but follower counts drift and accounts disappear (11 already did), so anything used for a real campaign should be re-checked first.
- The outreach emails are one-to-one business proposals with a real sender identity and reply address. Opt-outs should always be respected.
- No scraping behind logins, no ToS-breaking automation, no bought lists.
