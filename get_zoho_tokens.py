import os
import requests
import argparse
from dotenv import load_dotenv

# usage: python get_zoho_tokens.py <auth_code>

def get_zoho_tokens(auth_code: str):
    """Exchanges an authorization code for access and refresh tokens."""
    load_dotenv()

    client_id = os.getenv("ZOHO_CLIENT_ID")
    client_secret = os.getenv("ZOHO_CLIENT_SECRET")
    redirect_uri = os.getenv("ZOHO_REDIRECT_URI")
    accounts_url = os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com")

    if not all([client_id, client_secret, redirect_uri, auth_code]):
        raise ValueError("Missing one or more required parameters or environment variables.")

    url = f"{accounts_url}/oauth/v2/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": auth_code,
    }

    try:
        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "access_token" in data:
            print("✅ Token request successful!")
            print("Access Token:", data["access_token"])
            print("Refresh Token:", data.get("refresh_token"))
            print("Expires In:", data.get("expires_in"))
            print("API Domain:", data.get("api_domain"))
        else:
            print("⚠️ Unexpected response:", data)

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", str(e))
    except ValueError:
        print("❌ Failed to decode JSON response.")
    except Exception as e:
        print("❌ Unexpected error:", str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Zoho access and refresh tokens using auth code.")
    parser.add_argument(
        "auth_code",
        type=str,
        help="Authorization code received from Zoho OAuth"
    )
    args = parser.parse_args()

    get_zoho_tokens(args.auth_code)
