import json
from pathlib import Path


# =========================================================
# STORAGE
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CAMPAIGN_STORAGE_DIR = (
    BASE_DIR
    / "storage"
    / "campaigns"
)


# =========================================================
# ENSURE CAMPAIGN STORAGE
# =========================================================

def _ensure_campaign_storage():
    CAMPAIGN_STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# =========================================================
# CAMPAIGN TRACKING FILE
# =========================================================

def _get_tracking_file(campaign_id):
    _ensure_campaign_storage()

    return (
        CAMPAIGN_STORAGE_DIR
        / f"{campaign_id}.json"
    )


# =========================================================
# CREATE CAMPAIGN TRACKING
# =========================================================

def create_campaign_tracking(
    campaign_id,
    recipients,
    subject,
):
    """
    Create initial tracking data for a campaign.
    """

    tracking_file = _get_tracking_file(
        campaign_id
    )

    data = {
        "campaign_id": campaign_id,
        "subject": subject,
        "recipient_count": len(recipients),
        "recipients": {},
    }

    for email in recipients:

        email = email.strip().lower()

        if not email:
            continue

        data["recipients"][email] = {
            "status": "draft_created",
            "draft_id": None,
            "message_id": None,
            "thread_id": None,
        }

    tracking_file.write_text(
        json.dumps(
            data,
            indent=4,
        ),
        encoding="utf-8",
    )

    return data


# =========================================================
# GET CAMPAIGN TRACKING
# =========================================================

def get_campaign_tracking(campaign_id):
    """
    Return tracking data for a campaign.
    """

    tracking_file = _get_tracking_file(
        campaign_id
    )

    if not tracking_file.exists():
        return None

    return json.loads(
        tracking_file.read_text(
            encoding="utf-8"
        )
    )

# =========================================================
# UPDATE RECIPIENT TRACKING
# =========================================================

def update_campaign_recipient(
    campaign_id,
    email,
    draft_id=None,
    message_id=None,
    thread_id=None,
    status="draft_created",
):
    """
    Update tracking information for one campaign recipient.
    """

    tracking_file = _get_tracking_file(
        campaign_id
    )

    if not tracking_file.exists():
        raise ValueError(
            "Campaign tracking record not found"
        )

    data = json.loads(
        tracking_file.read_text(
            encoding="utf-8"
        )
    )

    email = email.strip().lower()

    if email not in data["recipients"]:
        raise ValueError(
            "Recipient not found in campaign tracking"
        )

    recipient = data["recipients"][email]

    recipient["status"] = status

    if draft_id is not None:
        recipient["draft_id"] = draft_id

    if message_id is not None:
        recipient["message_id"] = message_id

    if thread_id is not None:
        recipient["thread_id"] = thread_id

    tracking_file.write_text(
        json.dumps(
            data,
            indent=4,
        ),
        encoding="utf-8",
    )

    return recipient