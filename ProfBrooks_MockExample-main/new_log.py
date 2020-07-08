import requests
import logging
from datetime import datetime

URL = 'http://localhost:5001'


def log_event(user_id, username, details):
    post_url = URL + "/api/activities"
    new_activity = {
        "user_id": 1,
        "username": username,
        "timestamp": str(datetime.utcnow()),
        "details": details,
    }
    try:
        r = requests.post(post_url, json=new_activity)
        if r.status_code == 201:
            logging.info(f"Post new activity SUCCESS at {post_url}")
        else:
            logging.critical(f"Post new activity FAILURE: {r.text}")
    except requests.exceptions.RequestException:
        logging.critical(f"Could not connect to activity log service at {URL}")


def do_something_interesting():
    log_event(1, "testing", "Did something interesting")
    return True


if __name__ == '__main__':
    do_something_interesting()
