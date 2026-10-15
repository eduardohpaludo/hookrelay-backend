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
        print(f"Failed, Status code: {result['status_code']}, Message: {result['error']}")
    

def send_webhook(url, payload):
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=5)
        response.raise_for_status()
        return {"ok": True, "status_code": response.status_code, "error": None}
    
    except requests.exceptions.HTTPError as http_error:
        return {"ok": False, "status_code": response.status_code, "error": str(http_error)}
    except requests.exceptions.Timeout as conn_timeout:
        return {"ok": False, "status_code": None, "error": str(conn_timeout)}
    except requests.exceptions.ConnectionError as conn_error:
        return {"ok": False, "status_code": None, "error": str(conn_error)}

if __name__ == "__main__":
    main()