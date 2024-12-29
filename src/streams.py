import time
import json
import requests

access_file = open("access.secret", "r")
access_token, refresh_token, expires_at = access_file.read().strip().split(",")

rf = open("data/summary_activity/1.json")
content = rf.read()
jc = json.loads(content)

aid = jc[1]["id"]
print(aid)

url = "https://www.strava.com/api/v3/activities/{id}/streams".format(id = str(aid))
payload = {
    "keys": "time,distance,latlng,altitude,heartrate,velocity_smooth,cadence,watts,temp,moving,grade_smooth",
    "key_by_type": "true"}
headers = {"Authorization": "Bearer " + access_token}
r = requests.get(url, params=payload, headers=headers)
wf = open("data/streams/{id}.json".format(id = str(aid)), "w")
wf.write(r.text)
wf.close()
print(r.url)
print(r.text)
