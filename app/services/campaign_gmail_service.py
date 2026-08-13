from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


# =========================================================
# CREATE CAMPAIGN GMAIL DRAFT
# =========================================================

def create_campaign_gmail_draft(
    credentials,
    to_email,
    bcc_emails,
    subject,
    body,
):
    """
    Create one Gmail draft.

    First recipient is placed in TO.
    Remaining recipients are placed in BCC.
    """

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
    )

    message = MIMEText(
        body,
        "plain",
        "utf-8",
    )

    message["To"] = to_email
    message["Subject"] = subject

    if bcc_emails:

        message["Bcc"] = ", ".join(
            bcc_emails
        )

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft_body = {
        "message": {
            "raw": raw_message,
        }
    }

    draft = (
        service.users()
        .drafts()
        .create(
            userId="me",
            body=draft_body,
        )
        .execute()
    )

    return draft