"""Central configuration for the micro-influencer outreach system."""

# ---- Brand running the campaign (demo brand for this assignment) ----
BRAND_NAME = "UrbanNest"
BRAND_TAGLINE = "a D2C lifestyle brand for young Indian households"
BRAND_WEBSITE = "https://urbannest.example.in"
SENDER_NAME = "Abhishek Bahmani"
SENDER_ROLE = "Creator Partnerships"
SENDER_EMAIL = "abhishekbahmani303@gmail.com"

# ---- Micro-influencer definition ----
MIN_FOLLOWERS = 5_000
MAX_FOLLOWERS = 100_000

# ---- Engagement-rate benchmarks (India, micro tier) used when the
#      directory did not report a real ER. Clearly labelled "estimated". ----
ER_BENCHMARKS = [
    (5_000, 20_000, 4.0),
    (20_000, 50_000, 3.0),
    (50_000, 100_001, 2.2),
]

# ---- Per-niche collaboration playbook used for personalization ----
NICHE_PLAYBOOK = {
    "Lifestyle": {
        "collab_type": "UGC + barter collaboration",
        "short_collab": "UGC collab",
        "product_line": "our new home & living collection",
        "value_prop": "authentic everyday styling for young Indian homes",
        "offer": "gifted products plus a per-deliverable UGC fee",
    },
    "Travel": {
        "collab_type": "sponsored post + affiliate campaign",
        "short_collab": "sponsored travel campaign",
        "product_line": "our travel-organizer and gear range",
        "value_prop": "practical gear stories told from real Indian journeys",
        "offer": "a flat sponsorship fee plus 12% affiliate commission",
    },
    "Tech": {
        "collab_type": "paid review + affiliate campaign",
        "short_collab": "paid gadget review",
        "product_line": "our smart-home accessories range",
        "value_prop": "honest, spec-driven reviews your audience trusts",
        "offer": "a paid review fee, review units, and affiliate commission",
    },
    "Food": {
        "collab_type": "sponsored post + barter collaboration",
        "short_collab": "sponsored tasting collab",
        "product_line": "our gourmet pantry & kitchenware line",
        "value_prop": "credible local food storytelling",
        "offer": "a sponsorship fee plus a full product hamper",
    },
    "Fitness": {
        "collab_type": "brand ambassador program",
        "short_collab": "paid ambassador program",
        "product_line": "our activewear & clean-nutrition line",
        "value_prop": "science-first fitness content for Indian audiences",
        "offer": "a monthly retainer, free products, and affiliate earnings",
    },
}

# ---- SMTP (Gmail) settings for the sending layer ----
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465          # SSL
DRY_RUN_DEFAULT = True   # never send unless explicitly asked

# ---- File paths ----
RAW_CSV = "data/influencers_raw.csv"
ENRICHED_CSV = "output/influencers_enriched.csv"
SEGMENT_CSV = "output/segment_lifestyle_travel.csv"
MESSAGES_CSV = "output/outreach_messages.csv"
EMAILS_MD = "output/email_templates.md"
DMS_MD = "output/instagram_dm_templates.md"
