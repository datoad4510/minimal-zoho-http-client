import os
import requests
import time
from dotenv import load_dotenv


# Load env once at the top
load_dotenv()

# Module-level variables
access_token = None
access_token_expiry = 0  # UNIX timestamp
refresh_threshold = 300  # 5 minutes before expiry, refresh

CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
ACCOUNTS_URL = os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com")
API_DOMAIN = os.getenv("API_DOMAIN", "https://www.zohoapis.com")

def refresh_access_token():
    """
    Refreshes Zoho access token using refresh token from .env.
    Updates module-level access_token and access_token_expiry.
    """
    global access_token, access_token_expiry

    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        raise ValueError("Missing required environment variables for token refresh.")

    url = f"{ACCOUNTS_URL}/oauth/v2/token"
    params = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    try:
        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("🔹 Refresh token response:", data)

        if "access_token" not in data:
            raise ValueError(f"Failed to refresh token. Response: {data}")

        access_token = data["access_token"]
        access_token_expiry = time.time() + int(data.get("expires_in", 3600)) - refresh_threshold
        print("✅ Access token refreshed successfully.")

    except Exception as e:
        print("❌ Failed to refresh access token:", str(e))
        raise


# wrapper that checks if the access token is expired and refreshes it if it is
def get_access_token():
    if access_token is None or time.time() >= access_token_expiry:
        refresh_access_token()
    return access_token

def call_zoho_custom_api(endpoint: str, params: dict = None, payload: dict = None, method: str = "GET"):
    """
    Calls a Zoho Creator custom API endpoint.
    """
    access_token = get_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request(
            method=method.upper(),
            url=endpoint,
            headers=headers,
            params=params,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        return {"error": f"HTTP {response.status_code}", "details": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}
    except ValueError:
        return {"error": "Invalid JSON response", "details": response.text}


if __name__ == "__main__":
    load_dotenv()
    api_domain = os.getenv("API_DOMAIN", "https://www.zohoapis.com")

    print(access_token)
    print(api_domain)

    # your custom endpoint
    endpoint = f"{api_domain}/creator/custom/bcxcrm/HelloWorld_TEST"

    print("👉 Calling Zoho Creator custom API...")
    result = call_zoho_custom_api(endpoint)
    print("✅ Response:", result)
