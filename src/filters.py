"""
Step 2 — Segmentation.

Builds filtered segments from the enriched dataset. The assignment requires
at least one segment; we ship two examples:
  * segment_lifestyle_travel.csv — Lifestyle + Travel creators, verified email,
    ER >= 2.0 (the primary outreach segment for UrbanNest's home/travel lines)
  * a summary of counts per niche is printed for reference.
"""

import csv
from collections import Counter

from config import ENRICHED_CSV, SEGMENT_CSV


def load():
    with open(ENRICHED_CSV, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def segment(rows, niches=("Lifestyle", "Travel"), min_er=2.0, email_required=True):
    out = []
    for r in rows:
        if r["niche"] not in niches:
            continue
        if email_required and r["email_status"] != "verified_public":
            continue
        if float(r["engagement_rate_pct"]) < min_er:
            continue
        out.append(r)
    return out


def main():
    rows = load()
    print("Niche counts:", dict(Counter(r["niche"] for r in rows)))
    seg = segment(rows)
    with open(SEGMENT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(seg)
    print(f"-> segment 'Indian Lifestyle & Travel, verified email, ER>=2%': "
          f"{len(seg)} creators -> {SEGMENT_CSV}")


if __name__ == "__main__":
    main()
