# AI Cold Email Automation

## Business Concept

AI Cold Email Automation helps businesses scale professional outreach without manually preparing every email campaign.

The system combines company knowledge, prospect data, and a simple natural-language instruction to generate relevant campaign emails and prepare Gmail drafts automatically.

Its ultimate purpose is to turn repetitive cold-email work into a structured and scalable business workflow.

---

## Project Overview

The system allows a user to:

1. Authenticate with Google/Gmail.
2. Upload a company Knowledge Base PDF.
3. Upload a recipient CSV.
4. Provide a natural-language campaign instruction.
5. Generate an AI-powered campaign using the Knowledge Base.
6. Create Gmail drafts for recipient batches.
7. Track campaign and recipient information.

---

## Business Value

This project is more than an AI email generator.

It connects company knowledge, prospect data, AI content generation, Gmail, and campaign tracking into a single outreach automation workflow.

The result is a reusable foundation for businesses that want to reduce repetitive email work, maintain consistent messaging, and scale professional outreach more efficiently.

---

### Core Workflow

Knowledge Base PDF +
Recipient CSV +
Natural Client Instruction
↓
AI Generation
↓
Campaign Email
↓
Gmail Draft
↓
Campaign Tracking

---

## Key Features

- Google OAuth authentication
- Knowledge Base PDF upload and management
- Recipient CSV upload
- Email validation and duplicate handling
- Natural-language campaign instructions
- AI-generated subject and email body
- Knowledge Base-grounded content generation
- Gmail draft creation
- Recipient batching up to 250 recipients
- TO/BCC handling
- Campaign ID generation
- Gmail draft/message/thread tracking
- Recipient-level campaign tracking

---

## Architecture

```text
Client
│
├── Knowledge Base
├── Recipient List
└── Campaign Instruction
        │
        ▼
FastAPI Backend
        │
   ┌────┴────┐
   ▼         ▼
OpenAI     Storage
   │         │
   │         ├── Campaigns
   │         ├── Recipients
   │         └── Knowledge Base
   │
   ▼
Campaign Content
        │
        ▼
Gmail API
        │
        ▼
Gmail Draft
        │
        ▼
Campaign Tracking


---

## Project Structure

app/
├── api/
│   └── campaign.py
├── auth/
│   └── google_auth.py
├── config/
│   └── google/
│       └── settings.py
├── services/
│   ├── campaign_ai_service.py
│   ├── campaign_gmail_service.py
│   ├── campaign_tracking_service.py
│   ├── ai_service.py
│   ├── gmail_service.py
│   └── email_tracking_service.py
└── main.py

storage/
├── campaigns/
├── knowledge_base/
└── recipients/
```

### Important Modules

- `app/main.py` — FastAPI application and router registration
- `app/api/campaign.py` — Campaign and recipient API endpoints
- `app/auth/google_auth.py` — Google authentication
- `app/config/google/settings.py` — Google environment configuration
- `app/services/campaign_ai_service.py` — AI campaign generation
- `app/services/campaign_gmail_service.py` — Gmail campaign operations
- `app/services/campaign_tracking_service.py` — Campaign tracking

---

## API Endpoints

| Endpoint                           | Purpose                            |
| ---------------------------------- | ---------------------------------- |
| `GET /`                            | API health check                   |
| `GET /auth/login`                  | Start Google authentication        |
| `GET /auth/callback`               | Handle Google OAuth callback       |
| `POST /knowledge-base/upload`      | Upload Knowledge Base PDF          |
| `GET /knowledge-base/`             | View Knowledge Base status         |
| `DELETE /knowledge-base/`          | Remove Knowledge Base              |
| `POST /campaign/upload-recipients` | Upload recipient CSV               |
| `GET /campaign/recipients`         | View recipients                    |
| `DELETE /campaign/recipients`      | Remove recipient data              |
| `POST /campaign/generate-drafts`   | Generate campaign and Gmail drafts |

---

## AI & Knowledge Base

The client does not need to write technical AI prompts.

A natural instruction such as:

"Write a professional email explaining what diabetes is and how it can be managed."

can be provided directly.

The system uses the uploaded Knowledge Base internally to provide relevant context to the AI.

For example, a diabetes-related Knowledge Base can provide information about diabetes, management, complications, monitoring, and treatment when generating a campaign email.

---

## Gmail Campaign Flow

The system generates the campaign content and distributes recipients into manageable batches.

- Maximum batch size: 250 recipients
- First recipient is placed in `TO`
- Remaining recipients are placed in `BCC`
- Each batch creates a Gmail draft
- Gmail `draft_id`, `message_id`, and `thread_id` are captured

---

## Campaign Tracking

Every campaign receives a unique `campaign_id`.

Recipient-level tracking stores:

campaign_id
recipient
status
draft_id
message_id
thread_id

This allows the system to maintain campaign state for individual recipients and preserve Gmail-related identifiers.

---

## Technology Stack

- Python
- FastAPI
- OpenAI API
- Gmail API
- Google OAuth
- Pydantic
- CSV processing
- JSON-based campaign tracking
- Local file storage

---

## Current Project Status

### Completed

- Google authentication
- Environment configuration
- Knowledge Base PDF upload
- Recipient CSV processing
- Email validation
- AI campaign generation
- Knowledge Base-based generation
- Gmail draft creation
- Recipient batching
- TO/BCC handling
- Campaign tracking
- Draft/message/thread ID tracking
- End-to-end campaign draft testing

---

## Example Business Use Case

A company uploads its service or company information as a Knowledge Base PDF and provides a list of prospects through CSV.

The client then enters a simple instruction such as:

"Write a professional email explaining our services and how they can help potential clients."

The system uses the company information to generate the campaign, prepares Gmail drafts for the prospects, and stores campaign tracking information.

---

## Future Expansion

Potential future extensions include:

- Automated campaign sending
- Email open and reply tracking
- Campaign dashboard
- Advanced personalization
- Scheduled campaigns
- Multiple Knowledge Bases
- Database-backed analytics
- Production deployment

---


