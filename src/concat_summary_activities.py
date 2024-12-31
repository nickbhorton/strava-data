import json
from os import listdir

data_path = "data/summary_activity/"

concat_filenames = []
for filename in listdir(data_path):
    fileparts = filename.split('.')
    if fileparts[-1] == "json" and fileparts[0].isdigit():
        concat_filenames.append(".".join(fileparts))

total_jc = []
for filename in concat_filenames:
    file = open(data_path + filename, "r")
    for obj in json.loads(file.read()):
        total_jc.append(obj)
    file.close()

allfile = open(data_path + "all.json", "w")
allfile.write(json.dumps(total_jc))
allfile.close()
