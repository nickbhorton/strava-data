import time
import pickle
import requests
import random
from os import listdir

access_token = '4b369d37eceeff2a6a92bb7f69ffea33175703a2'

ids = open("act2024/ids.txt", "r")
ids = ids.read().split()

file_names = listdir("./act2024/alts")
computed_ids = []
for fn in file_names:
    if fn.split(".")[1] == "json":
        computed_ids.append(fn.split(".")[0])

uncomputed_ids = []
for id in ids:
    if id not in computed_ids:
        uncomputed_ids.append(id)

print(len(uncomputed_ids), "ids left")
for i in range(16,92):
    id = uncomputed_ids[i]
    print(i, id)
    url = "https://www.strava.com/api/v3/activities/{id}/streams".format(id = id)
    payload = {"keys": ["altitude"], "key_by_type": "true"}
    headers = {"Authorization": "Bearer " + access_token}
    # r = requests.get(url, params=payload, headers=headers)
    if r.status_code != 200:
        print(r.status_code)
        print(r.url)
        print(r.text)
    else:
        print(len(r.text))
        f = open("act2024/alts/{id}.json".format(id = id), "w")
        f.write(r.text)
