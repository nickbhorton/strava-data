import time
import json
import requests
from os import listdir

access_file = open("access.secret", "r")
access_token, refresh_token, expires_at = access_file.read().strip().split(",")

api_reads_file = open("api_reads.txt", "r")
daily_reads, chunk_reads = api_reads_file.read().strip().split(",")
api_reads_file.close()

daily_reads = int(daily_reads)
chunk_reads = int(chunk_reads)
print("daily reads:", daily_reads)
print("reads in this 15 minutes:", chunk_reads)

proc_ids_fn = listdir("data/streams")
proc_ids = []
for s in proc_ids_fn:
    proc_ids.append(int(s.split(".")[0]))
print(proc_ids)

rf = open("data/summary_activity/all.json", "r")
jc = json.loads(rf.read())
rf.close()

keys = ["time","distance","latlng","altitude","velocity_smooth","heartrate","cadence","watts","temp","moving","grade_smooth"]

payload = {
    "keys": ",".join(keys),
    "key_by_type": "true"
}
headers = {"Authorization": "Bearer " + access_token}

for obj in jc:
    if daily_reads == 1000:
        break
    if chunk_reads == 100:
        print(time.ctime())
        cmin = int(time.ctime()[14:16])
        nmin = 60
        if cmin < 15:
            nmin = 15
        elif cmin < 30:
            nmin = 30
        elif cmin < 45:
            nmin = 45
        print(abs(cmin - nmin))
        wait_sec = abs(cmin - nmin) * 60 + 15
        print("waiting for", wait_sec, "seconds")
        time.sleep(wait_sec)
        print(time.ctime())
        chunk_reads = 0

    aid = obj["id"]
    if aid in proc_ids:
        continue
    if obj["manual"]:
        print(aid, "manual")
        continue
    url = "https://www.strava.com/api/v3/activities/{id}/streams".format(id = str(aid))
    r = requests.get(url, params=payload, headers=headers)
    daily_reads += 1
    chunk_reads += 1
    stream_jc = json.loads(r.text)
    print(aid, "", end="")
    for key in keys:
        if key in stream_jc:
            print(key, "", end="")
    print()
    wf = open("data/streams/{id}.json".format(id = str(aid)), "w")
    wf.write(r.text)
    wf.close()

api_reads_file = open("api_reads.txt", "w")
api_reads_file.write(",".join([str(daily_reads), str(chunk_reads)]))
api_reads_file.close()


