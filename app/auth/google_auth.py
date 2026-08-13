from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from google_auth_oauthlib.flow import Flow

from app.config.google.settings import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)


router = APIRouter(
    prefix="/auth",
    tags=["Google Auth"],
)


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def create_flow() -> Flow:
    client_config = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                GOOGLE_REDIRECT_URI,
            ],
        }
    }

    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )


@router.get("/login")
def google_login(request: Request):
    flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session["oauth_state"] = state
    request.session["oauth_code_verifier"] = flow.code_verifier

    return RedirectResponse(url=authorization_url)


@router.get("/callback")
def google_callback(
    request: Request,
    code: str,
    state: str,
):
    saved_state = request.session.get("oauth_state")
    saved_code_verifier = request.session.get(
        "oauth_code_verifier"
    )

    if not saved_state:
        return JSONResponse(
            status_code=400,
            content={"error": "OAuth state not found"},
        )

    if state != saved_state:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid OAuth state"},
        )

    if not saved_code_verifier:
        return JSONResponse(
            status_code=400,
            content={
                "error": "OAuth code verifier not found"
            },
        )

    flow = create_flow()
    flow.code_verifier = saved_code_verifier

    try:
        flow.fetch_token(code=code)

        credentials = flow.credentials

        request.session["access_token"] = credentials.token
        request.session["refresh_token"] = (
            credentials.refresh_token
        )

        request.session.pop("oauth_state", None)
        request.session.pop(
            "oauth_code_verifier",
            None,
        )

        return RedirectResponse(url="/")

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Google authentication failed",
                "details": str(e),
            },
        )