import time
import pickle
import requests

access_token = '4b369d37eceeff2a6a92bb7f69ffea33175703a2'

epoch_now = 1735216121
epoch_year_begin = 1704092400

url = "https://www.strava.com/api/v3/athlete/activities"
payload = {"before": epoch_now, "after": epoch_year_begin, "page": 3, "per_page": 200}
headers = {"Authorization": "Bearer " + access_token}
r = requests.get(url, params=payload, headers=headers)
print(r.text)