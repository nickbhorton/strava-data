import json
import time
from dateutil.parser import isoparse
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

rf = open("data/summary_activity/all.json", "r")
content = rf.read()
jc = json.loads(content)

tmt = {
    "2019": 0, 
    "2020": 0, 
    "2021": 0, 
    "2022": 0, 
    "2023": 0, 
    "2024": 0,  
}
tet = {
    "2019": 0, 
    "2020": 0, 
    "2021": 0, 
    "2022": 0, 
    "2023": 0, 
    "2024": 0,  
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
    moving_time = obj["moving_time"]
    elapsed_time = obj["elapsed_time"]
    # 2024
    if epoch_time > s2024 and epoch_time < now:
        tmt["2024"] += moving_time
        tet["2024"] += elapsed_time
    elif epoch_time > s2023 and epoch_time < s2024:
        tmt["2023"] += moving_time
        tet["2023"] += elapsed_time
    elif epoch_time > s2022 and epoch_time < s2023:
        tmt["2022"] += moving_time
        tet["2022"] += elapsed_time
    elif epoch_time > s2021 and epoch_time < s2022:
        tmt["2021"] += moving_time
        tet["2021"] += elapsed_time
    elif epoch_time > s2020 and epoch_time < s2021:
        tmt["2020"] += moving_time
        tet["2020"] += elapsed_time
    elif epoch_time > s2019 and epoch_time < s2020:
        tmt["2019"] += moving_time
        tet["2019"] += elapsed_time
    else:
        print("time weird")

tmt_lst = [tmt["2024"],tmt["2023"],tmt["2022"],tmt["2021"],tmt["2020"],tmt["2019"]]
tet_lst = [tet["2024"],tet["2023"],tet["2022"],tet["2021"],tet["2020"],tet["2019"]]
year_lst = [2024, 2023, 2022, 2021, 2020, 2019]

for i in range(len(tmt_lst)):
    tmt_lst[i] /= 60 * 60
    tet_lst[i] /= 60 * 60

fig, ax = plt.subplots()
width = 0.25
ax.bar(year_lst, tmt_lst, width = width, color = "r", label = "Moving Time")
ax.bar([year_lst[i] + width for i in range(len(year_lst))], tet_lst, width = width, color = "b", label = "Elapsed Time")
plt.xticks([year_lst[i] + width/2 for i in range(len(year_lst))], ['2024','2023','2022','2021','2020','2019'])
plt.xlabel("Year")
plt.ylabel("Hours")
plt.legend()
plt.show()

print("total moving time", tmt)
print("total elapsed time", tet)
