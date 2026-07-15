"""Pipeline orchestrator: enrich -> segment -> personalize -> (dry-run) send."""
import enrichment
import filters
import personalize
import send_emails

if __name__ == "__main__":
    print("== Step 2+3: enrichment & filtering ==")
    enrichment.enrich()
    print("\n== Step 2: segmentation ==")
    filters.main()
    print("\n== Step 4: personalization ==")
    personalize.main()
    print("\n== Step 5: sending layer (dry-run preview, first 5) ==")
    send_emails.send_batch(send=False, limit=5)
