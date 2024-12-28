import json
from os import listdir

data_root = "act2024/alts/"
data_send_root = "act2024/alts_data/"

file_names = listdir("./act2024/alts")
ids = []
for fn in file_names:
    if fn.split(".")[1] == "json":
        ids.append(fn.split(".")[0])

for id in ids:
    print(id)
    test_id = id

    json_file = open(data_root + test_id + ".json", "r")
    content = json_file.read()
    json_file.close()

    json_content = json.loads(content)
    if json_content.get("distance") == None:
        continue
    if json_content.get("altitude") == None:
        continue
    distance = json_content["distance"]["data"]
    altitude = json_content["altitude"]["data"]

    out_file = open(data_send_root + str(id) + ".data", "w")

    for i in range(len(altitude)):
        out_file.write(str(distance[i]))
        out_file.write(" ")
        out_file.write(str(altitude[i]))
        out_file.write("\n")

    out_file.close()
