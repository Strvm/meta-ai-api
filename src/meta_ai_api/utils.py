import logging
import random
import time
from typing import Dict, Optional

from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup

from meta_ai_api.exceptions import FacebookInvalidCredentialsException


def generate_offline_threading_id() -> str:
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


def extract_value(text: str, start_str: str, end_str: str) -> str:
    """
    Helper function to extract a specific value from the given text using a key.

    Args:
        text (str): The text from which to extract the value.
        start_str (str): The starting key.
        end_str (str): The ending key.

    Returns:
        str: The extracted value.
    """
    start = text.find(start_str) + len(start_str)
    end = text.find(end_str, start)
    return text[start:end]


def format_response(response: dict) -> str:
    """
    Formats the response from Meta AI to remove unnecessary characters.

    Args:
        response (dict): The dictionnary containing the response to format.

    Returns:
        str: The formatted response.
    """
    text = ""
    for content in (
        response.get("data", {})
        .get("node", {})
        .get("bot_response_message", {})
        .get("composed_text", {})
        .get("content", [])
    ):
        text += content["text"] + "\n"
    return text


# Function to perform the login
def get_fb_session(email, password, proxies=None):
    login_url = "https://www.facebook.com/login/?next"
    headers = {
        "authority": "mbasic.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    # Send the GET request
    response = requests.get(login_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")

    # Parse necessary parameters from the login form
    lsd = soup.find("input", {"name": "lsd"})["value"]
    jazoest = soup.find("input", {"name": "jazoest"})["value"]

    # Define the URL and body for the POST request to submit the login form
    post_url = "https://www.facebook.com/login/?next"
    data = {
        "lsd": lsd,
        "jazoest": jazoest,
        "login_source": "comet_headerless_login",
        "email": email,
        "pass": password,
        "login": "1",
        "next": None,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": None,
        "Referer": "https://www.facebook.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.facebook.com",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "cookie": f"datr={response.cookies.get('datr')};",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
    }

    from requests import cookies

    # Send the POST request
    session = requests.session()
    jar = cookies.RequestsCookieJar()
    session.proxies = proxies
    session.cookies = jar

    result = session.post(post_url, headers=headers, data=data)
    if "sb" not in jar or "xs" not in jar:
        raise FacebookInvalidCredentialsException(
            "Was not able to login to Facebook. Please check your credentials. "
            "You may also have been rate limited. Try to connect to Facebook manually."
        )

    cookies = {
        **result.cookies.get_dict(),
        "sb": jar["sb"],
        "xs": jar["xs"],
        "fr": jar["fr"],
        "c_user": jar["c_user"],
    }

    response_login = {
        "cookies": cookies,
        "headers": result.headers,
        "response": response.text,
    }
    meta_ai_cookies = get_cookies()

    url = "https://www.meta.ai/state/"

    payload = f'__a=1&lsd={meta_ai_cookies["lsd"]}'
    headers = {
        "authority": "www.meta.ai",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f'ps_n=1; ps_l=1; dpr=2; _js_datr={meta_ai_cookies["_js_datr"]}; abra_csrf={meta_ai_cookies["abra_csrf"]}; datr={meta_ai_cookies["datr"]};; ps_l=1; ps_n=1',
        "origin": "https://www.meta.ai",
        "pragma": "no-cache",
        "referer": "https://www.meta.ai/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, proxies=proxies
    )

    state = extract_value(response.text, start_str='"state":"', end_str='"')

    url = f"https://www.facebook.com/oidc/?app_id=1358015658191005&scope=openid%20linking&response_type=code&redirect_uri=https%3A%2F%2Fwww.meta.ai%2Fauth%2F&no_universal_links=1&deoia=1&state={state}"
    payload = {}
    headers = {
        "authority": "www.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": f"datr={response_login['cookies']['datr']}; sb={response_login['cookies']['sb']}; c_user={response_login['cookies']['c_user']}; xs={response_login['cookies']['xs']}; fr={response_login['cookies']['fr']}; abra_csrf={meta_ai_cookies['abra_csrf']};",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    session = requests.session()
    session.proxies = proxies
    response = session.get(url, headers=headers, data=payload, allow_redirects=False)

    next_url = response.headers["Location"]

    url = next_url

    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.meta.ai/",
        "Connection": "keep-alive",
        "Cookie": f'dpr=2; abra_csrf={meta_ai_cookies["abra_csrf"]}; datr={meta_ai_cookies["_js_datr"]}',
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
    }
    session.get(url, headers=headers, data=payload)
    cookies = session.cookies.get_dict()
    if "abra_sess" not in cookies:
        raise FacebookInvalidCredentialsException(
            "Was not able to login to Facebook. Please check your credentials. "
            "You may also have been rate limited. Try to connect to Facebook manually."
        )
    logging.info("Successfully logged in to Facebook.")
    return cookies


def get_cookies() -> dict:
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


def get_session(
    proxy: Optional[Dict] = None, test_url: str = "https://api.ipify.org/?format=json"
) -> requests.Session:
    """
    Get a session with the proxy set.

    Args:
        proxy (Dict): The proxy to use
        test_url (str): A test site from which we check that the proxy is installed correctly.

    Returns:
        requests.Session: A session with the proxy set.
    """
    session = requests.Session()
    if not proxy:
        return session
    response = session.get(test_url, proxies=proxy, timeout=10)
    if response.status_code == 200:
        session.proxies = proxy
        return session
    else:
        raise Exception("Proxy is not working.")
