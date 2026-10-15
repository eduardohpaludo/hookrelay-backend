import requests
from requests.exceptions import HTTPError, Timeout


def send_webhook(url, payload):
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=5)
        response.raise_for_status()
        print(response.status_code)

    except HTTPError as http_error:
        print(f"Http error occurred: {http_error}")
    except Timeout as conn_timeout:
        print(f"Timeout occurred: {conn_timeout}")
    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection Error: {conn_error}")

webhook_url = 'https://webhook.site/72ac2923-0394-4ccf-b954-95122ba2a640'

payload = {
    "event": "user.signup",
    "data": {
        "user_id": 123,
        "email": "test@example.com"
    }
}

if __name__ == "__main__":
    send_webhook(webhook_url, payload=payload)