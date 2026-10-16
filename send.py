import requests
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url is None:
        print("Webhook url is not defined, check your .env file")
        return
    
    payload = {
        "event": "user.signup",
        "data": {
            "user_id": 123,
            "email": "test@example.com"
        }
    }
    
    result = send_webhook(webhook_url, payload=payload)
    if result["ok"]:
        print(f"Succeeded, Status code: {result['status_code']}")
    else:
        retryable = "permanent"
        if result['retryable']:
            retryable = "retryable"
        print(f"Failed, Status code: {result['status_code']}, Message: {result['error']}, Retryable: {retryable}")

def is_retryable_status(status_code):
    if status_code >= 500 and status_code < 600:
        return True
    elif status_code == 408 or status_code == 429:
        return True
    return False
    

def send_webhook(url, payload):
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=5)
        response.raise_for_status()
        return {"ok": True, "status_code": response.status_code, "error": None, "retryable": False}
    
    except requests.exceptions.HTTPError as http_error:
        retryable = is_retryable_status(response.status_code)
        return {"ok": False, "status_code": response.status_code, "error": str(http_error), "retryable": retryable}
    except requests.exceptions.Timeout as conn_timeout:
        return {"ok": False, "status_code": None, "error": str(conn_timeout), "retryable": True}
    except requests.exceptions.ConnectionError as conn_error:
        return {"ok": False, "status_code": None, "error": str(conn_error), "retryable": True}

if __name__ == "__main__":
    main()