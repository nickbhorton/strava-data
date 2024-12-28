import json
from os import listdir
import matplotlib.pyplot as plt

data_root = "act2024/alts/"

file_names = listdir("./act2024/alts")
ids = []
for fn in file_names:
    if fn.split(".")[1] == "json":
        ids.append(fn.split(".")[0])

test_id = ids[202]
print(test_id)

json_file = open(data_root + test_id + ".json", "r")
content = json_file.read()
json_file.close()

json_content = json.loads(content)
distance = json_content["distance"]["data"]
altitude = json_content["altitude"]["data"]
for i in range(len(distance)):
    distance[i] *= 0.000621371
for i in range(len(altitude)):
    altitude[i] *= 3.28084

plt.plot(distance, altitude)
plt.xlabel("distance (miles)")
plt.ylabel("altitude (feet)")


new_dist = []
new_alt = []
avg_window = 10
for i in range(len(distance) // avg_window):
    avg_dist = 0
    avg_alt = 0
    for j in range(avg_window):
        avg_dist += distance[i * avg_window + j]
        avg_alt += altitude[i * avg_window + j]
    avg_dist /= avg_window
    avg_alt /= avg_window
    new_dist.append(avg_dist)
    new_alt.append(avg_alt)

last_avg_dist = 0
last_avg_alt = 0
for i in range(len(distance) % avg_window):
    last_avg_dist += distance[len(distance) - 1 - i]
    last_avg_alt  += altitude[len(distance) - 1 - i]

last_avg_dist /= len(distance) % avg_window
last_avg_alt /= len(distance) % avg_window

new_dist.append(last_avg_dist)
new_alt.append(last_avg_alt)

plt.plot(new_dist, new_alt)

first_alt = new_alt[0]
for i in range(len(new_alt)):
    new_alt[i] -= first_alt

plt.plot(new_dist, new_alt)


plt.show()


