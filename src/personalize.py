"""
Step 4 — Message personalization.

For every influencer generates:
  A. an outreach email (validated 60-90 words)
  B. an Instagram DM (validated 15-30 words)

Personalization inputs: niche (collab type/product/value prop from
NICHE_PLAYBOOK), creator's content themes, city, platform and handle.
Outputs: output/outreach_messages.csv + human-readable markdown files.
"""

import csv

from config import (BRAND_NAME, BRAND_TAGLINE, DMS_MD, EMAILS_MD,
                    ENRICHED_CSV, MESSAGES_CSV, NICHE_PLAYBOOK, SENDER_NAME,
                    SENDER_ROLE)


def first_name(name: str) -> str:
    clean = name.split("(")[0].strip()
    return clean.split()[0] if clean else "there"


def wc(text: str) -> int:
    return len(text.split())


def themes_phrase(row) -> str:
    themes = [t.strip() for t in row["content_themes"].split(";") if t.strip()]
    return " and ".join(themes[:2]) if themes else row["niche"].lower()


def city_clause(row) -> str:
    city = row["city_state"].split(",")[0].strip()
    return f" from {city}" if city and city != "India" else ""


def build_email(row) -> dict:
    p = NICHE_PLAYBOOK[row["niche"]]
    fname = first_name(row["name"])
    platform = row["platforms"].split(";")[0].strip()
    body = (
        f"Hi {fname},\n\n"
        f"I came across your {platform} ({row['handle']}) and really enjoyed your "
        f"{themes_phrase(row)} content{city_clause(row)} — it captures exactly the "
        f"{p['value_prop']} we want to champion. I'm {SENDER_NAME}, {SENDER_ROLE} at "
        f"{BRAND_NAME}, {BRAND_TAGLINE}. We're launching {p['product_line']} and would "
        f"love to partner with you on a {p['collab_type']}. You keep full creative "
        f"freedom; we offer {p['offer']}. Would you be open to a quick call this week?\n\n"
        f"Best,\n{SENDER_NAME}, {BRAND_NAME}"
    )
    # enforce 60-90 words on the body copy
    if wc(body) < 60:
        body = body.replace("Would you be open",
                            "Happy to share the full brief and payment terms upfront. "
                            "Would you be open")
    if wc(body) > 90:  # compact variant for verbose niches (e.g. Travel)
        body = (
            f"Hi {fname},\n\n"
            f"I loved your {themes_phrase(row)} content{city_clause(row)} on {platform} "
            f"({row['handle']}) — exactly the {p['value_prop']} we want to champion. "
            f"I'm {SENDER_NAME} from {BRAND_NAME}. We're launching {p['product_line']} "
            f"and would love to partner with you on a {p['collab_type']}. We offer "
            f"{p['offer']}, and creative control stays fully with you. "
            f"Open to a quick call this week?\n\n"
            f"Best,\n{SENDER_NAME}, {BRAND_NAME}"
        )
    assert 60 <= wc(body) <= 90, f"email out of range ({wc(body)}w) for {row['handle']}"
    subject = f"{BRAND_NAME} x {row['handle']} — {p['short_collab']}?"
    return {"subject": subject, "email_body": body, "email_words": wc(body)}


def build_dm(row) -> dict:
    p = NICHE_PLAYBOOK[row["niche"]]
    fname = first_name(row["name"])
    dm = (f"Hi {fname}! Love your {themes_phrase(row)} posts. I'm from {BRAND_NAME} — "
          f"we're planning a {p['short_collab']} with Indian {row['niche'].lower()} "
          f"creators and you'd be a great fit. Open to details?")
    if wc(dm) > 30:  # shorten for long theme phrases
        dm = (f"Hi {fname}! Love your {row['niche'].lower()} content. I'm from {BRAND_NAME} — "
              f"planning a {p['short_collab']} and you'd be a great fit. Open to details?")
    assert 15 <= wc(dm) <= 30, f"DM out of range ({wc(dm)}w) for {row['handle']}"
    return {"instagram_dm": dm, "dm_words": wc(dm)}


def main():
    with open(ENRICHED_CSV, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    out_rows, email_md, dm_md = [], [], []
    for row in rows:
        email = build_email(row)
        dm = build_dm(row)
        out_rows.append({
            "name": row["name"], "handle": row["handle"], "niche": row["niche"],
            "contact_email": row["contact_email"], "email_status": row["email_status"],
            **email, **dm,
        })
        email_md.append(f"### {row['name']} ({row['handle']}, {row['niche']})\n"
                        f"**To:** {row['contact_email'] or 'DM only — no public email'}\n"
                        f"**Subject:** {email['subject']}\n\n{email['email_body']}\n")
        dm_md.append(f"**{row['name']}** ({row['handle']}, {row['niche']}):\n"
                     f"> {dm['instagram_dm']}\n")

    with open(MESSAGES_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    with open(EMAILS_MD, "w", encoding="utf-8") as fh:
        fh.write(f"# Personalized outreach emails ({len(out_rows)} creators)\n\n" + "\n".join(email_md))
    with open(DMS_MD, "w", encoding="utf-8") as fh:
        fh.write(f"# Personalized Instagram DMs ({len(out_rows)} creators)\n\n" + "\n".join(dm_md))
    print(f"-> {len(out_rows)} personalized emails (60-90w) + DMs (15-30w) written to "
          f"{MESSAGES_CSV}, {EMAILS_MD}, {DMS_MD}")


if __name__ == "__main__":
    main()
