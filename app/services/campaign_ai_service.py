import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing"
    )


# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# =========================================================
# GENERATE CAMPAIGN EMAIL
# =========================================================

def generate_campaign_email(
    instruction,
    recipient,
    knowledge_base_file_id=None,
):
    """
    Generate one campaign email using the
    uploaded company Knowledge Base PDF.

    The campaign email is generated once and
    reused for all recipient batches.
    """

    if not instruction:
        raise ValueError(
            "Campaign instruction is required"
        )

    if not knowledge_base_file_id:
        raise ValueError(
            "Knowledge Base file is required"
        )

    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an AI cold-email campaign writer.

You must create ONE professional cold email using
the attached Knowledge Base PDF as the source of
truth about the company.

CRITICAL INSTRUCTIONS:

1. READ THE ATTACHED KNOWLEDGE BASE DOCUMENT.
2. Extract the actual company information from it.
3. Use the actual company name from the document.
4. Use the actual services, products, expertise,
   capabilities, or other relevant information
   found in the document.
5. The final email must be ready to send.
6. NEVER use generic placeholders.
7. NEVER write:
   [Your Name]
   [Your Company Name]
   [Your Position]
   [Your Contact Information]
   [briefly list main services]
   [Your Services]
   or any similar placeholder.
8. Do not invent company facts that are not present
   in the Knowledge Base.
9. If the Knowledge Base does not contain a person's
   name, position, phone number, or email address,
   simply omit those details.
10. Do not invent recipient-specific information.
11. Keep the email professional and suitable for
    legitimate business outreach.

Campaign instruction:

{instruction}

Recipient:

{recipient}

OUTPUT REQUIREMENTS:

Return ONLY valid JSON.

The JSON must contain exactly two fields:

{{
    "subject": "...",
    "body": "..."
}}

Do not return markdown.
Do not return explanations.
Do not wrap the JSON in code fences.

Before producing the final JSON, make sure the body
contains actual information extracted from the
Knowledge Base and contains NO unresolved placeholders.
"""

    # -----------------------------------------------------
    # OPENAI REQUEST
    # -----------------------------------------------------

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_file",
                        "file_id": knowledge_base_file_id,
                    },
                ],
            }
        ],
    )

    result = (
        response.output_text
        .strip()
    )

    # -----------------------------------------------------
    # PARSE JSON
    # -----------------------------------------------------

    try:

        data = json.loads(
            result
        )

    except json.JSONDecodeError as e:

        raise ValueError(
            "AI returned invalid JSON"
        ) from e

    # -----------------------------------------------------
    # EXTRACT FIELDS
    # -----------------------------------------------------

    subject = (
        data.get(
            "subject",
            ""
        )
        .strip()
    )

    body = (
        data.get(
            "body",
            ""
        )
        .strip()
    )

    if not subject:
        raise ValueError(
            "AI returned empty subject"
        )

    if not body:
        raise ValueError(
            "AI returned empty body"
        )

    # -----------------------------------------------------
    # PLACEHOLDER VALIDATION
    # -----------------------------------------------------

    forbidden_placeholders = [
        "[Your Name]",
        "[Your Company Name]",
        "[Your Position]",
        "[Your Contact Information]",
        "[Your Services]",
        "[Your Company]",
        "[Company Name]",
        "[Your Name/Company]",
        "[briefly list main services]",
        "[briefly list main services or areas of expertise]",
    ]

    body_lower = body.lower()

    for placeholder in forbidden_placeholders:

        if placeholder.lower() in body_lower:

            raise ValueError(
                "AI generated unresolved placeholder: "
                + placeholder
            )

    # -----------------------------------------------------
    # BASIC GENERIC-TEMPLATE DETECTION
    # -----------------------------------------------------

    generic_phrases = [
        "my name is [",
        "on behalf of [",
        "our services include [",
        "contact me directly at [",
    ]

    for phrase in generic_phrases:

        if phrase in body_lower:

            raise ValueError(
                "AI generated a generic template "
                "instead of using Knowledge Base information"
            )

    # -----------------------------------------------------
    # RETURN NORMALIZED JSON
    # -----------------------------------------------------

    return json.dumps(
        {
            "subject": subject,
            "body": body,
        },
        ensure_ascii=False,
    )