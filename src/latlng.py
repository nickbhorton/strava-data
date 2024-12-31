import json
from os import listdir
import struct

datapath = "data/streams/"
files = listdir(datapath)
bf = open("data/all.lla", "wb")
bf.write(bytes(".LLA", "ascii"))
bf.write(struct.pack("@l", 1))

for filename in files:
    id = int(filename.split(".")[0])
    rf = open(datapath + filename)
    jc = json.loads(rf.read())
    if "latlng" in jc and "altitude" in jc:
        bf.write(struct.pack("@l", id))
        array_size = len(jc["latlng"]["data"])
        bf.write(struct.pack("@l", array_size))
        for i in range(array_size):
            lat, lng = jc["latlng"]["data"][i]
            alt = jc["altitude"]["data"][i]
            bin = struct.pack("@fff", lat, lng, alt)
            bf.write(bin)
    rf.close()
bf.close()
