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
plt.show()
