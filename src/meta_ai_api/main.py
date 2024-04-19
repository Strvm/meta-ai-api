import json
import random
import time
import urllib
import uuid

import requests
from requests_html import HTMLSession


class MetaAI:
    """
    A class to interact with the Meta AI API to obtain and use access tokens for sending
    and receiving messages from the Meta AI Chat API.
    """

    def __init__(self):
        self.session = requests.Session()
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
            "av": "0",
            "__user": "0",
            "__a": "1",
            "__req": "4",
            "__ccg": "UNKNOWN",
            "lsd": "AVrWIDJrQQI",
            "__jssesw": "1",
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAbraAcceptTOSForTempUserMutation",
            "variables": {
                "dob": "1999-01-01",
                "icebreaker_type": "TEXT",
                "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
            },
            "server_timestamps": "true",
            "doc_id": "7604648749596940",
        }
        payload = urllib.parse.urlencode(payload)
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'_js_datr={self.cookies["_js_datr"]}; abra_csrf={self.cookies["abra_csrf"]};',
            "dpr": "2",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "x-fb-friendly-name": "useAbraAcceptTOSForTempUserMutation",
            "x-fb-lsd": "AVrWIDJrQQI",
        }

        response = self.session.post(url, headers=headers, data=payload)
        auth_json = response.json()
        access_token = auth_json["data"]["xab_abra_accept_terms_of_service"][
            "new_temp_user_auth"
        ]["access_token"]
        return access_token

    def prompt(self, message: str, attempts: int = 0) -> str:
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
                    "offlineThreadingId": self.generate_offline_threading_id(),
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
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
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
            if streaming_state == "OVERALL_DONE":
                last_streamed_response = json_line

        if last_streamed_response is None:
            if attempts > 3:
                raise Exception(
                    "MetaAI is having issues and was not able to respond (Server Error)"
                )
            self.access_token = self.get_access_token()
            return self.prompt(message=message, attempts=attempts + 1)
        response = self.format_response(response=last_streamed_response)
        return response

    def get_cookies(self) -> dict:
        """
        Extracts necessary cookies from the Meta AI main page.

        Returns:
            dict: A dictionary containing essential cookies.
        """
        session = HTMLSession()
        response = session.get("https://www.meta.ai/")
        return {
            "_js_datr": self._extract_value(response.text, "_js_datr"),
            "abra_csrf": self._extract_value(response.text, "abra_csrf"),
        }

    def _extract_value(self, text: str, key: str) -> str:
        """
        Helper function to extract a specific value from the given text using a key.

        Args:
            text (str): The text from which to extract the value.
            key (str): The key associated with the value.

        Returns:
            str: The extracted value.
        """
        start = text.find(f'{key}":{{"value":"') + len(f'{key}":{{"value":"')
        end = text.find('",', start)
        return text[start:end]

    def format_response(self, response: dict) -> str:
        """
        Formats the response from Meta AI to remove unnecessary characters.

        Args:
            response (dict): The dictionnary containing the response to format.

        Returns:
            str: The formatted response.
        """
        text = ""
        for content in response["data"]["node"]["bot_response_message"][
            "composed_text"
        ]["content"]:
            text += content["text"] + "\n"
        return text

    def generate_offline_threading_id(self) -> str:
        """
        Generates an offline threading ID.

        Returns:
            str: The generated offline threading ID.
        """
        # Maximum value for a 64-bit integer in Python
        max_int = (1 << 64) - 1
        mask22_bits = (1 << 22) - 1

        # Function to get the current timestamp in milliseconds
        def get_current_timestamp():
            return int(time.time() * 1000)

        # Function to generate a random 64-bit integer
        def get_random_64bit_int():
            return random.getrandbits(64)

        # Combine timestamp and random value
        def combine_and_mask(timestamp, random_value):
            shifted_timestamp = timestamp << 22
            masked_random = random_value & mask22_bits
            return (shifted_timestamp | masked_random) & max_int

        timestamp = get_current_timestamp()
        random_value = get_random_64bit_int()
        threading_id = combine_and_mask(timestamp, random_value)

        return str(threading_id)


if __name__ == "__main__":
    meta = MetaAI()
    print(meta.prompt("Whats the weather in San Francisco today?"))
