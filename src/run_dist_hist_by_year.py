import json
import time
from dateutil.parser import isoparse
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

rf = open("data/summary_activity/all.json", "r")
content = rf.read()
jc = json.loads(content)

run_dists = {
    "2019": [], 
    "2020": [], 
    "2021": [], 
    "2022": [], 
    "2023": [], 
    "2024": [],  
}

s2024 = 1704067200
s2023 = 1672531200
s2022 = 1640995200
s2021 = 1609459200 
s2020 = 1577836800
s2019 = 1546300800
now = time.time()

for obj in jc:
    dt = obj["start_date"]
    epoch_time = int(isoparse(dt).timestamp())
    sport_type = obj["sport_type"]
    if sport_type == "Run":
        dist = obj["distance"] * 0.000621371
        # 2024
        if epoch_time > s2024 and epoch_time < now:
            run_dists["2024"].append(dist)
        elif epoch_time > s2023 and epoch_time < s2024:
            run_dists["2023"].append(dist)
        elif epoch_time > s2022 and epoch_time < s2023:
            run_dists["2022"].append(dist)
        elif epoch_time > s2021 and epoch_time < s2022:
            run_dists["2021"].append(dist)
        elif epoch_time > s2020 and epoch_time < s2021:
            run_dists["2020"].append(dist)
        elif epoch_time > s2019 and epoch_time < s2020:
            run_dists["2019"].append(dist)
        else:
            print("time weird")


fig, ax = plt.subplots(6,1)
ax[0].hist(run_dists["2024"], bins = [i for i in range(102)], edgecolor='black')
ax[0].set_title("2024")
ax[1].hist(run_dists["2023"], bins = [i for i in range(102)], edgecolor='black')
ax[1].set_title("2023")
ax[2].hist(run_dists["2022"], bins = [i for i in range(102)], edgecolor='black')
ax[2].set_title("2022")
ax[3].hist(run_dists["2021"], bins = [i for i in range(102)], edgecolor='black')
ax[3].set_title("2021")
ax[4].hist(run_dists["2020"], bins = [i for i in range(102)], edgecolor='black')
ax[4].set_title("2020")
ax[5].hist(run_dists["2019"], bins = [i for i in range(102)], edgecolor='black')
ax[5].set_title("2019")
"""
for count, bin_center in zip(counts, 0.5*(bins[:-1] + bins[1:])):
    lab = ""
    if (count > 0):
        lab = str(int(count))
    plt.annotate(lab, xy=(bin_center, count), xytext=(0, 3),textcoords="offset points", ha='center', va='bottom')
"""
plt.xlim(0,102)
plt.show()

