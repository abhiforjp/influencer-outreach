"""
Step 1 — Influencer discovery.

Discovers Indian micro-influencers from public creator directories and
hashtag/keyword searches. Sources actually used to build data/influencers_raw.csv:

  * Feedspot public directories (Indian Lifestyle / Travel / Food / Fitness /
    Yoga / Tech YouTube lists + city lists like Kolkata, Jaipur, Pune)
  * StarNgage free India category rankings (Technology, Cooking) — also gives
    engagement rates
  * Creators' own blogs / YouTube About pages / Facebook pages (for emails)
  * Web search of hashtags: #IndianFashion #IndianTravel #FitIndia
    #IndianFoodBlogger etc.

This module automates the directory part: give it a directory URL and it
extracts candidate creators. Manual verification is still expected — the
final dataset was human-verified row by row.
"""

import csv
import re
import sys

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; outreach-research/1.0)"}

DIRECTORY_SOURCES = [
    "https://influencers.feedspot.com/indian_lifestyle_instagram_influencers/",
    "https://influencers.feedspot.com/indian_travel_instagram_influencers/",
    "https://influencers.feedspot.com/indian_food_instagram_influencers/",
    "https://influencers.feedspot.com/indian_fitness_instagram_influencers/",
    "https://videos.feedspot.com/indian_tech_youtube_channels/",
    "https://starngage.com/plus/en-us/influencer/ranking/instagram/india/technology",
]

HASHTAG_QUERIES = [
    "#IndianFashion micro influencer", "#IndianTravel creator collaboration",
    "#FitIndia fitness creator", "#IndianFoodBlogger", "#SkincareIndia creator",
]

FOLLOWER_RE = re.compile(r"([\d.]+)\s*([KkMm]?)")


def parse_follower_count(text: str):
    """'94.7K' -> 94700, '1.2M' -> 1200000."""
    m = FOLLOWER_RE.search(text or "")
    if not m:
        return None
    num, suffix = float(m.group(1)), m.group(2).lower()
    return int(num * {"k": 1_000, "m": 1_000_000}.get(suffix, 1))


def scrape_feedspot_list(url: str):
    """Extract (name, handle, followers, location) candidates from a Feedspot list."""
    try:
        html = requests.get(url, headers=HEADERS, timeout=30).text
    except requests.RequestException as exc:
        print(f"  ! could not fetch {url}: {exc}", file=sys.stderr)
        return []
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    for block in soup.select("h3, .trow"):  # Feedspot list item headings/rows
        text = block.get_text(" ", strip=True)
        handle = None
        link = block.find("a", href=re.compile(r"instagram\.com|youtube\.com"))
        if link:
            handle = link["href"]
        followers = parse_follower_count(text)
        if handle and followers:
            candidates.append({
                "name": text.split("|")[0].strip()[:80],
                "profile_url": handle,
                "followers": followers,
                "source": url,
            })
    return candidates


def is_micro(followers: int, lo=5_000, hi=100_000) -> bool:
    return followers is not None and lo <= followers <= hi


def discover(out_path="output/discovered_candidates.csv"):
    """Run directory discovery and dump micro-tier candidates for manual review."""
    rows = []
    for url in DIRECTORY_SOURCES:
        print(f"* scraping {url}")
        rows += [c for c in scrape_feedspot_list(url) if is_micro(c["followers"])]
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["name", "profile_url", "followers", "source"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"-> {len(rows)} micro-tier candidates written to {out_path}")
    print("Hashtag queries to run manually on Instagram/Google:")
    for q in HASHTAG_QUERIES:
        print("   ", q)


if __name__ == "__main__":
    discover()
