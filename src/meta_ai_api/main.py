import json
import urllib
import uuid
from typing import Dict, List

import requests
from requests_html import HTMLSession

from meta_ai_api.utils import (
    generate_offline_threading_id,
    extract_value,
    format_response,
)


class MetaAI:
    """
    A class to interact with the Meta AI API to obtain and use access tokens for sending
    and receiving messages from the Meta AI Chat API.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            }
        )
        self.access_token = None
        self.cookies = None

    def get_access_token(self) -> str:
        """
        Retrieves an access token using Meta's authentication API.

        Returns:
            str: A valid access token.
        """
        self.cookies = self.get_cookies()
        url = "https://www.meta.ai/api/graphql/"

        payload = {
            "lsd": self.cookies["lsd"],
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAbraAcceptTOSForTempUserMutation",
            "variables": {
                "dob": "1999-01-01",
                "icebreaker_type": "TEXT",
                "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
            },
            "doc_id": "7604648749596940",
        }
        payload = urllib.parse.urlencode(payload)
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'_js_datr={self.cookies["_js_datr"]}; abra_csrf={self.cookies["abra_csrf"]}; datr={self.cookies["datr"]};',
            "sec-fetch-site": "same-origin",
            "x-fb-friendly-name": "useAbraAcceptTOSForTempUserMutation",
        }

        response = self.session.post(url, headers=headers, data=payload)
        auth_json = response.json()
        access_token = auth_json["data"]["xab_abra_accept_terms_of_service"][
            "new_temp_user_auth"
        ]["access_token"]
        return access_token

    def prompt(self, message: str, attempts: int = 0) -> Dict:
        """
        Sends a message to the Meta AI and returns the response.

        Args:
            message (str): The message to send.
            attempts (int): The number of attempts made (used for recursion).

        Returns:
            str: The received response from Meta AI.

        Raises:
            Exception: If unable to obtain a valid response after several attempts.
        """
        if not self.access_token:
            self.access_token = self.get_access_token()

        url = "https://graph.meta.ai/graphql?locale=user"
        payload = {
            "access_token": self.access_token,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAbraSendMessageMutation",
            "variables": json.dumps(
                {
                    "message": {"sensitive_string_value": message},
                    "externalConversationId": str(uuid.uuid4()),
                    "offlineThreadingId": generate_offline_threading_id(),
                    "suggestedPromptIndex": None,
                    "flashVideoRecapInput": {"images": []},
                    "flashPreviewInput": None,
                    "promptPrefix": None,
                    "entrypoint": "ABRA__CHAT__TEXT",
                    "icebreaker_type": "TEXT",
                    "__relay_internal__pv__AbraDebugDevOnlyrelayprovider": False,
                    "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
                }
            ),
            "server_timestamps": "true",
            "doc_id": "7783822248314888",
        }
        payload = urllib.parse.urlencode(payload)
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-fb-friendly-name": "useAbraSendMessageMutation",
        }

        response = self.session.post(url, headers=headers, data=payload)
        raw_response = response.text
        last_streamed_response = None
        for line in raw_response.split("\n"):
            try:
                json_line = json.loads(line)
            except json.JSONDecodeError:
                continue
            bot_response_message = (
                json_line.get("data", {})
                .get("node", {})
                .get("bot_response_message", {})
            )
            streaming_state = bot_response_message.get("streaming_state")
            fetch_id = bot_response_message.get("fetch_id")
            if streaming_state == "OVERALL_DONE":
                last_streamed_response = json_line

        if last_streamed_response is None:
            if attempts > 3:
                raise Exception(
                    "MetaAI is having issues and was not able to respond (Server Error)"
                )
            self.access_token = self.get_access_token()
            return self.prompt(message=message, attempts=attempts + 1)
        response = format_response(response=last_streamed_response)
        sources = self.fetch_sources(fetch_id)
        return {"message": response, "sources": sources}

    def get_cookies(self) -> dict:
        """
        Extracts necessary cookies from the Meta AI main page.

        Returns:
            dict: A dictionary containing essential cookies.
        """
        session = HTMLSession()
        response = session.get("https://www.meta.ai/")
        return {
            "_js_datr": extract_value(
                response.text, start_str='_js_datr":{"value":"', end_str='",'
            ),
            "abra_csrf": extract_value(
                response.text, start_str='abra_csrf":{"value":"', end_str='",'
            ),
            "datr": extract_value(
                response.text, start_str='datr":{"value":"', end_str='",'
            ),
            "lsd": extract_value(
                response.text, start_str='"LSD",[],{"token":"', end_str='"}'
            ),
        }

    def fetch_sources(self, fetch_id: str) -> List[Dict]:
        """
        Fetches sources from the Meta AI API based on the given query.

        Args:
            fetch_id (str): The fetch ID to use for the query.

        Returns:
            list: A list of dictionaries containing the fetched sources.
        """

        url = "https://graph.meta.ai/graphql?locale=user"
        payload = {
            "access_token": self.access_token,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AbraSearchPluginDialogQuery",
            "variables": json.dumps({"abraMessageFetchID": fetch_id}),
            "server_timestamps": "true",
            "doc_id": "6946734308765963",
        }

        payload = urllib.parse.urlencode(payload)

        headers = {
            "authority": "graph.meta.ai",
            "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'dpr=2; abra_csrf={self.cookies["abra_csrf"]}; datr={self.cookies["datr"]}; ps_n=1; ps_l=1',
            "x-fb-friendly-name": "AbraSearchPluginDialogQuery",
        }

        response = self.session.post(url, headers=headers, data=payload)
        response_json = response.json()
        search_results = response_json["data"]["message"]["searchResults"]
        if search_results is None:
            return []

        references = search_results["references"]
        return references


if __name__ == "__main__":
    meta = MetaAI()
    print(meta.prompt("What was the Warriors score last game?"))
