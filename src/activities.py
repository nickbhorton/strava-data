import time
import requests
import json

access_file = open("access.secret", "r")
access_token, refresh_token, expires_at = access_file.read().strip().split(",")

page_number = 2
while True:
    url = "https://www.strava.com/api/v3/athlete/activities"
    payload = {"before": int(time.time()), "after": 0, "page": page_number, "per_page": 200}
    headers = {"Authorization": "Bearer " + access_token}
    r = requests.get(url, params=payload, headers=headers)
    print(r.url)
    wf = open("data/summary_activity/{page_number}.json".format(page_number = page_number), "w")
    wf.write(r.text)
    wf.close()

    page_number += 1
    jc = json.loads(r.text)
    print(len(jc))
    if len(jc) != 200:
        quit()
