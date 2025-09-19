import os
import time
from endpoints import Endpoints
from typing import TypeVar, Type
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
from endpoints import Endpoints
import json
import apiSchemas
from utils import print_types
from apiSchemas import OrderToJSONRequest



Req = TypeVar("Req", bound=BaseModel)
Res = TypeVar("Res", bound=BaseModel)

class ZohoCreatorClient:
    """
    Simplified Zoho Creator client for custom API functions.
    Assumes all endpoints are under /creator/custom/bcxcrm/{function_name}.
    """

    def __init__(self, client_id=None, client_secret=None, refresh_token=None,
                 accounts_url=None, api_domain=None, refresh_threshold=300):
        load_dotenv()

        # Config
        self.client_id = client_id or os.getenv("ZOHO_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("ZOHO_CLIENT_SECRET")
        self.refresh_token = refresh_token or os.getenv("REFRESH_TOKEN")
        self.accounts_url = accounts_url or os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com")
        self.api_domain = api_domain or os.getenv("API_DOMAIN", "https://www.zohoapis.com")

        if not all([self.client_id, self.client_secret, self.refresh_token]):
            raise ValueError("❌ Missing required Zoho OAuth environment variables.")

        # Token state
        self.access_token = None
        self.access_token_expiry = 0
        self.refresh_threshold = refresh_threshold

    def _refresh_access_token(self):
        """Refresh the Zoho access token using the refresh token."""
        url = f"{self.accounts_url}/oauth/v2/token"
        params = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
        }

        response = requests.post(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "access_token" not in data:
            raise ValueError(f"Failed to refresh token. Response: {data}")

        self.access_token = data["access_token"]
        self.access_token_expiry = time.time() + int(data.get("expires_in", 3600)) - self.refresh_threshold

    def _get_access_token(self):
        """Return a valid access token (refresh if expired)."""
        if self.access_token is None or time.time() >= self.access_token_expiry:
            self._refresh_access_token()
        return self.access_token

    def call_function(self, function_name: str, method: str = "GET",
                      params: dict = None, payload: dict = None):
        """
        Call a Zoho Creator custom api endpoint under /creator/custom/bcxcrm.

        :param function_name: Name of the custom api endpoint (e.g. "HelloWorld_TEST").
        :param method: HTTP method ("GET" or "POST").
        :param params: Query string parameters.
        :param payload: JSON body (for POST).
        """
        token = self._get_access_token()
        url = f"{self.api_domain}/creator/custom/bcxcrm/{function_name}"

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                json=payload,
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            return {"error": f"HTTP {response.status_code}", "details": response.text}
        except requests.exceptions.RequestException as e:
            return {"error": "Request failed", "details": str(e)}
        except ValueError:
            return {"error": "Invalid JSON response", "details": response.text}
        

    def call_typed(
    self,
    endpoint: Endpoints,
    request: Req,
    method: str = "POST"
) -> Res:
        # Get the expected request/response models
        req_model, res_model = apiSchemas.endpoint_schemas[endpoint]

        # Validate request type
        if not isinstance(request, req_model):
            raise TypeError(f"Expected {req_model.__name__}, got {type(request).__name__}")

        # Prepare request payload
        payload_or_params = request.model_dump()
        params = payload_or_params if method.upper() == "GET" else None
        payload = payload_or_params if method.upper() == "POST" else None

        # Call the generic API
        result = self.call_function(str(endpoint), method=method, params=params, payload=payload)

        # Check for error dicts returned by call_function
        if "error" in result:
            print("🔴 Zoho API Error Details:")
            for k, v in result.items():
                print(f"{k}: {v}")
            raise RuntimeError(f"Zoho API Error: {result['error']}")

        # Parse response into typed model (Pydantic v2)
        return res_model.model_validate(result)


if __name__ == "__main__":
    client = ZohoCreatorClient()

    req = OrderToJSONRequest(orderID=3541189000008268029)

    res: apiSchemas.OrderToJSONResponse = client.call_typed(
        endpoint=Endpoints.ORDER_TO_JSON,
        request=req,
        method="GET"
    )

    print(res.result)
    print("\n\n\n")
    print(print_types(res.result))