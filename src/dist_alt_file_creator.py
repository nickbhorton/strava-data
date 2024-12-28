import json
from os import listdir

data_root = "act2024/alts/"
data_send_root = "act2024/alts_data/"

file_names = listdir("./act2024/alts")
ids = []
for fn in file_names:
    if fn.split(".")[1] == "json":
        ids.append(fn.split(".")[0])

act_discription_file = open("act2024/total.json", "r")
act_disc_content = act_discription_file.read()
act_json = json.loads(act_disc_content)

date_id_pair = []

for obj in act_json:
    date_str = obj["start_date"]
    month = date_str[5:7]
    day = date_str[8:10]
    sort_val = (int(month) * 40) + int(day)
    id = obj["id"]
    if str(id) in ids:
        date_id_pair.append([sort_val, id])

date_id_pair.sort()
# print(date_id_pair)

fail_count = 0
for index in range(len(date_id_pair)):
    print(date_id_pair[index][1])
    test_id = str(date_id_pair[index][1])

    json_file = open(data_root + test_id + ".json", "r")
    content = json_file.read()
    json_file.close()

    json_content = json.loads(content)
    if json_content.get("distance") == None:
        fail_count += 1
        continue
    if json_content.get("altitude") == None:
        fail_count += 1
        continue
    distance = json_content["distance"]["data"]
    altitude = json_content["altitude"]["data"]

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

    if (len(distance) % avg_window != 0):
        last_avg_dist /= len(distance) % avg_window
        last_avg_alt /= len(distance) % avg_window

        new_dist.append(last_avg_dist)
        new_alt.append(last_avg_alt)

    first_alt = new_alt[0]
    for i in range(len(new_alt)):
        new_alt[i] -= first_alt

    out_file = open(data_send_root + str(index - fail_count) + ".data", "w")

    for i in range(len(new_dist)):
        out_file.write(str(new_dist[i]))
        out_file.write(" ")
        out_file.write(str(new_alt[i]))
        out_file.write("\n")

    out_file.close()
