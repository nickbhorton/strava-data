import json
import time
from dateutil.parser import isoparse
import matplotlib.pyplot as plt

rf = open("data/summary_activity/all.json", "r")
content = rf.read()
jc = json.loads(content)

counts = []
time = []

for obj in jc:
    dt = obj["start_date"]
    epoch_time = int(isoparse(dt).timestamp())
    year = int(dt[:4])
    month = int(dt[5:7])
    day = int(dt[8:10])
    hour = int(dt[11:13])
    minute = int(dt[14:16])
    second = int(dt[17:19])
    counts.append(obj["kudos_count"])
    time.append(epoch_time)

plt.scatter(time, counts)
plt.show()
