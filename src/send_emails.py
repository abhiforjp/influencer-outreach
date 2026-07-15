"""
Step 5 — Sending layer.

Sends the personalized emails over Gmail SMTP (SSL). SAFE BY DEFAULT:
runs in dry-run mode and only prints what WOULD be sent. To actually send:

    export SMTP_USER="you@gmail.com"
    export SMTP_PASS="your-gmail-app-password"   # not your login password
    python send_emails.py --send [--limit 5] [--test-to you@gmail.com]

Instagram DMs are intentionally NOT automated: unofficial IG DM automation
violates Instagram's Terms of Use. DM copy is exported ready-to-paste, or can
be pushed through an approved partner platform (e.g. Meta API via an official
Instagram messaging partner) — see README.
"""

import argparse
import csv
import os
import smtplib
import sys
import time
from email.mime.text import MIMEText

from config import DRY_RUN_DEFAULT, MESSAGES_CSV, SENDER_EMAIL, SENDER_NAME, SMTP_HOST, SMTP_PORT


def load_messages():
    with open(MESSAGES_CSV, newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["email_status"] == "verified_public"]


def send_batch(send=False, limit=None, test_to=None):
    msgs = load_messages()
    if limit:
        msgs = msgs[:limit]
    dry = not send or DRY_RUN_DEFAULT and not send

    server = None
    if send:
        user, password = os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASS")
        if not (user and password):
            sys.exit("Set SMTP_USER and SMTP_PASS environment variables first.")
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(user, password)

    for i, m in enumerate(msgs, 1):
        to_addr = test_to or m["contact_email"]
        print(f"[{i}/{len(msgs)}] {'DRY-RUN' if dry else 'SENDING'} -> {to_addr}  "
              f"({m['name']}, {m['niche']})  subject: {m['subject']}")
        if dry:
            continue
        mime = MIMEText(m["email_body"], "plain", "utf-8")
        mime["Subject"] = m["subject"]
        mime["From"] = f"{SENDER_NAME} <{os.environ['SMTP_USER']}>"
        mime["To"] = to_addr
        mime["Reply-To"] = SENDER_EMAIL
        server.sendmail(os.environ["SMTP_USER"], [to_addr], mime.as_string())
        time.sleep(3)  # polite rate limit

    if server:
        server.quit()
    print(f"Done. {len(msgs)} messages {'previewed (dry-run)' if dry else 'sent'}.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="actually send (default: dry-run)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--test-to", default=None, help="override recipient (send all to yourself)")
    args = ap.parse_args()
    send_batch(send=args.send, limit=args.limit, test_to=args.test_to)
