import json

import requests
from requests_html import HTMLSession


class MetaAI:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = self.get_access_token()

    def get_access_token(self):
        cookies = self.get_cookies()
        url = "https://www.meta.ai/api/graphql/"

        payload = "av=0&__user=0&__a=1&__req=4&__ccg=UNKNOWN&lsd=AVrWIDJrQQI&__jssesw=1&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=useAbraAcceptTOSForTempUserMutation&variables=%7B%22dob%22%3A%221999-01-01%22%2C%22icebreaker_type%22%3A%22TEXT%22%2C%22__relay_internal__pv__WebPixelRatiorelayprovider%22%3A1%7D&server_timestamps=true&doc_id=7604648749596940"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'_js_datr={cookies["_js_datr"]}; abra_csrf={cookies["abra_csrf"]};',
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

    def get_cookies(self):
        # Need to make this much cleaner
        session = HTMLSession()
        r = session.get("https://www.meta.ai/")
        raw_text = r.text
        _js_datr_start = raw_text.find('_js_datr":{"value":"')
        _js_datr_end = raw_text.find('",', _js_datr_start)
        _js_datr = raw_text[_js_datr_start:_js_datr_end].replace(
            '_js_datr":{"value":"', ""
        )

        abra_csrf_start = raw_text.find('abra_csrf":{"value":"')
        abra_csrf_end = raw_text.find('",', abra_csrf_start)
        abra_csrf = raw_text[abra_csrf_start:abra_csrf_end].replace(
            'abra_csrf":{"value":"', ""
        )
        return {"_js_datr": _js_datr, "abra_csrf": abra_csrf}

    def prompt(self, message: str):
        url = "https://graph.meta.ai/graphql?locale=user"

        payload = f"av=0&access_token={self.access_token}&__user=0&__a=1&__req=p&__hs=19831.HYP%3Aabra_pkg.2.1..0.0&dpr=1&__ccg=UNKNOWN&__s=%3A0ryskm%3Aewvpqb&__comet_req=46&lsd=AVrLt4uZ-4k&__spin_b=trunk&__jssesw=1&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=useAbraSendMessageMutation&variables=%7B%22message%22%3A%7B%22sensitive_string_value%22%3A%22{message}%22%7D%2C%22externalConversationId%22%3A%22dae20bda-6450-4ce7-880c-1db1b3ae7da3%22%2C%22offlineThreadingId%22%3A%227186784311738402039%22%2C%22suggestedPromptIndex%22%3Anull%2C%22flashVideoRecapInput%22%3A%7B%22images%22%3A%5B%5D%7D%2C%22flashPreviewInput%22%3Anull%2C%22promptPrefix%22%3Anull%2C%22entrypoint%22%3A%22ABRA__CHAT__TEXT%22%2C%22icebreaker_type%22%3A%22TEXT%22%2C%22__relay_internal__pv__AbraDebugDevOnlyrelayprovider%22%3Afalse%2C%22__relay_internal__pv__WebPixelRatiorelayprovider%22%3A1%7D&server_timestamps=true&doc_id=7783822248314888"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "x-fb-friendly-name": "useAbraSendMessageMutation",
        }

        response = self.session.post(url, headers=headers, data=payload)
        raw_response = response.text
        last_streamed_response = None
        text = ""
        for line in raw_response.split("\n"):
            json_line = json.loads(line)
            if "errors" not in json_line.keys():
                last_streamed_response = json_line
        for content in last_streamed_response["data"]["node"]["bot_response_message"][
            "composed_text"
        ]["content"]:
            text += content["text"] + "\n"
        return text


if __name__ == "__main__":
    meta = MetaAI()
    print(meta.prompt("What was the match results for PSG vs Barca on April 16th"))
