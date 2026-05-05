"""Extract AD-Group IDs from Cisco Secure Access for use in policy rules.

Endpoint: GET https://api.sse.cisco.com/reports/v2/identities
Required OAuth scope: reports.utilities:read

Reads credentials from .env (API_KEY, API_SECRET, optional TOKEN_URL).
Writes:
  - identities-all.json   raw response (all identities, all types)
  - ad-groups.json        filtered AD groups: [{id, label, type}]
"""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"

DEFAULT_TOKEN_URL = "https://api.sse.cisco.com/auth/v2/token"
IDENTITIES_URL = "https://api.sse.cisco.com/reports/v2/identities"

REQUIRED_SCOPE = "reports.utilities:read"

# Identity type strings that represent AD groups in the Reporting API.
# Some tenants surface them as "ad_groups"; broaden if your data uses a
# different label (run once unfiltered and inspect identities-all.json).
AD_GROUP_TYPES = {"ad_groups"}


def get_token(token_url: str, client_id: str, client_secret: str) -> str:
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, auth=auth)
    return token["access_token"]


def token_scopes(access_token: str) -> list[str]:
    """Best-effort decode of a JWT body to read the granted scopes."""
    try:
        body = access_token.split(".")[1]
        body += "=" * (-len(body) % 4)
        claims = json.loads(base64.urlsafe_b64decode(body))
    except Exception:
        return []
    raw = claims.get("scope") or claims.get("scp") or ""
    if isinstance(raw, list):
        return raw
    return raw.split()


def fetch_all_identities(access_token: str, page_size: int = 5000) -> list[dict]:
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    out: list[dict] = []
    offset = 0

    while True:
        params = {"limit": page_size, "offset": offset}
        resp = requests.get(IDENTITIES_URL, headers=headers, params=params, timeout=30)

        if resp.status_code == 403:
            scopes = token_scopes(access_token)
            scope_msg = ", ".join(scopes) if scopes else "(none readable)"
            sys.exit(
                f"403 from {IDENTITIES_URL}.\n"
                f"Token scopes: {scope_msg}\n"
                f"Required scope: {REQUIRED_SCOPE}\n"
                "Add 'Reports > Utilities > Read-Only' to the API key in the SSE "
                "dashboard (Admin > API Keys), then re-run."
            )
        resp.raise_for_status()

        page = resp.json()
        items = page.get("data", []) or []
        out.extend(items)

        if len(items) < page_size:
            break
        offset += page_size

    return out


def filter_ad_groups(identities: list[dict]) -> list[dict]:
    ad_groups = []
    for item in identities:
        t = (item.get("type") or {}).get("type")
        if t in AD_GROUP_TYPES:
            ad_groups.append({"id": item.get("id"), "label": item.get("label"), "type": t})
    return ad_groups


def main() -> None:
    load_dotenv(ENV_PATH)

    client_id = os.environ.get("API_KEY")
    client_secret = os.environ.get("API_SECRET")
    token_url = os.environ.get("TOKEN_URL") or DEFAULT_TOKEN_URL

    if not client_id or not client_secret:
        sys.exit("API_KEY and API_SECRET must be set in .env")

    print(f"Fetching token from {token_url} ...")
    access_token = get_token(token_url, client_id, client_secret)

    scopes = token_scopes(access_token)
    if scopes and REQUIRED_SCOPE not in scopes:
        print(
            f"Warning: token scopes do not include {REQUIRED_SCOPE}. "
            "The /reports/v2/identities call will likely return 403.",
            file=sys.stderr,
        )

    print(f"Listing identities from {IDENTITIES_URL} ...")
    identities = fetch_all_identities(access_token)
    print(f"  retrieved {len(identities)} identities")

    out_dir = Path(__file__).resolve().parent
    (out_dir / "identities-all.json").write_text(
        json.dumps({"data": identities}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    ad_groups = filter_ad_groups(identities)
    (out_dir / "ad-groups.json").write_text(
        json.dumps(ad_groups, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"  wrote {out_dir / 'identities-all.json'}")
    print(f"  wrote {out_dir / 'ad-groups.json'}  ({len(ad_groups)} AD groups)")

    if ad_groups:
        ids = [g["id"] for g in ad_groups]
        print("\nAD-Group IDs (paste into umbrella.source.identity_ids):")
        print(json.dumps(ids))
    else:
        print(
            "\nNo identities matched AD_GROUP_TYPES="
            f"{sorted(AD_GROUP_TYPES)}. Inspect identities-all.json to see the "
            "type strings your tenant returns and adjust AD_GROUP_TYPES."
        )


if __name__ == "__main__":
    main()
