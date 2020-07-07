#!/usr/bin/env python
import click
import requests
import json
import time
from datetime import datetime


def _get_users(url):
    get_url = url + "/api/activities/"
    try:
        r = requests.get(get_url)
        if r.status_code == 200:
            print(f"Get activities SUCCESS at {get_url}")
            activities = json.loads(r.text)
            single_activity_id = 0
            if isinstance(activities, dict):
                if "activities" in activities:
                    single_activity_id = activities["activities"][0]["id"]
                elif "activity_log" in activities:
                    single_activity_id = activities["activity_log"][0]["id"]
                elif "Activity_Log" in activities:
                    single_activity_id = activities["Activity_Log"][0]["id"]
                elif "activityLog" in activities:
                    single_activity_id = activities["activityLog"][0]["id"]
                elif "users" in activities:
                    single_activity_id = activities["users"][0]["id"]
                else:
                    single_activity_id = activities["activitylog"][0]["id"]
            elif isinstance(activities, list):
                single_activity_id = activities[0]["id"]
            else:
                print("Error: JSON returned from Get neither list nor dict")
            r = requests.get(get_url + str(single_activity_id))
            if r.status_code == 200:
                print(f"    Get single activity {single_activity_id} SUCCESS")
                print(json.loads(r.text))
            else:
                print(f"Get single activity FAILURE: {r.text}")
        else:
            print(f"Get activities FAILURE: {r.text}")
    except requests.exceptions.RequestException:
        print(f"Could not connect to activity log service at {url}")


def _new_user(url):
    post_url = url + "/api/activities"
    new_activity = {
        "user_id": 9,
        "username": "Paul",
        "timestamp": str(datetime.utcnow()),
        "details": "Paul is alive",
    }
    try:
        r = requests.post(post_url, json=new_activity)
        if r.status_code == 201 or 200:
            print(f"Post new activity SUCCESS at {post_url}")
            print(r.text)
            print(json.loads(r.text))
        else:
            print(f"Post new activity FAILURE: {r.text}")
    except requests.exceptions.RequestException:
        print(f"Could not connect to activity log service at {url}")


@click.command()
@click.argument("url", type=click.STRING)
@click.option(
    "--sleep",
    "-s",
    default=1,
    help="number of seconds to sleep between requests"
)
def activity_logger(url, sleep):

    while True:
        _get_users(url)
        _new_user(url)
        time.sleep(sleep)


if __name__ == "__main__":
    activity_logger()
