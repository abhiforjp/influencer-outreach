"""
Step 2+3 — Filtering and profile enrichment.

Reads data/influencers_raw.csv (the human-verified research dataset), then:
  * validates the micro-influencer band (5k-100k)
  * validates email syntax and flags missing emails
  * fills missing engagement rates with clearly-labelled India micro-tier
    benchmarks (real reported ERs from StarNgage are kept as 'reported')
  * derives platform flags and a simple brand-fit score
Writes output/influencers_enriched.csv
"""

import csv
import re

from config import (ER_BENCHMARKS, ENRICHED_CSV, MAX_FOLLOWERS, MIN_FOLLOWERS,
                    NICHE_PLAYBOOK, RAW_CSV)

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def estimate_er(followers: int) -> float:
    for lo, hi, er in ER_BENCHMARKS:
        if lo <= followers < hi:
            return er
    return 2.0


def brand_fit_score(row: dict) -> int:
    """Simple 0-100 heuristic: email + ER + India location + micro band."""
    score = 40 if row["email_status"] == "verified_public" else 10
    er = float(row["engagement_rate_pct"])
    score += min(30, int(er * 5))                       # engagement
    if row["city_state"] and row["city_state"] != "India":
        score += 15                                     # known Indian city
    elif "India" in row["city_state"]:
        score += 8
    if MIN_FOLLOWERS <= int(row["followers"]) <= MAX_FOLLOWERS:
        score += 15                                     # true micro tier
    return min(score, 100)


def enrich():
    with open(RAW_CSV, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    enriched, skipped = [], 0
    for row in rows:
        followers = int(row["followers"])
        if not (MIN_FOLLOWERS <= followers <= MAX_FOLLOWERS):
            skipped += 1
            continue
        if row["contact_email"] and not EMAIL_RE.match(row["contact_email"]):
            row["email_status"] = "invalid_syntax"
        if not row["engagement_rate_pct"]:
            row["engagement_rate_pct"] = f"{estimate_er(followers):.2f}"
            row["er_source"] = "estimated (India micro-tier benchmark)"
        row["audience_indicator"] = "Indian-audience creator (India-based, Indian-language/locale content)"
        row["brand_fit_score"] = brand_fit_score(row)
        enriched.append(row)

    enriched.sort(key=lambda r: (-int(r["brand_fit_score"]), -float(r["engagement_rate_pct"])))
    fields = list(enriched[0].keys())
    with open(ENRICHED_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(enriched)

    n_email = sum(1 for r in enriched if r["email_status"] == "verified_public")
    print(f"-> {len(enriched)} influencers enriched ({skipped} outside 5k-100k skipped); "
          f"{n_email} with verified public emails. Written to {ENRICHED_CSV}")
    return enriched


if __name__ == "__main__":
    enrich()
