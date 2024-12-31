import json
import struct
from dateutil.parser import isoparse
import datetime
from os import listdir

sa_file = open("data/summary_activity/all.json", "r")
sa_jc = json.loads(sa_file.read())
sa_file.close()

data_items = []

sport_type_enum = {
    "AlpineSki": 9,
    "BackcountrySki": 0,
    "Badminton": 0,
    "Canoeing": 0,
    "Crossfit": 0,
    "EBikeRide": 0,
    "Elliptical": 0,
    "EMountainBikeRide": 0,
    "Golf": 0,
    "GravelRide": 0,
    "Handcycle": 0,
    "HighIntensityIntervalTraining": 0,
    "Hike": 2,
    "IceSkate": 0,
    "InlineSkate": 12,
    "Kayaking": 0,
    "Kitesurf": 0,
    "MountainBikeRide": 0,
    "NordicSki": 0,
    "Pickleball": 0,
    "Pilates": 0,
    "Racquetball": 0,
    "Ride": 3,
    "RockClimbing": 10,
    "RollerSki": 0,
    "Rowing": 11,
    "Run": 1,
    "Sail": 0,
    "Skateboard": 0,
    "Snowboard": 0,
    "Snowshoe": 0,
    "Soccer": 4,
    "Squash": 0,
    "StairStepper": 0,
    "StandUpPaddling": 0,
    "Surfing": 0,
    "Swim": 13,
    "TableTennis": 0,
    "Tennis": 0,
    "TrailRun": 0,
    "Velomobile": 0,
    "VirtualRide": 0,
    "VirtualRow": 0,
    "VirtualRun": 0,
    "Walk": 5,
    "WeightTraining": 6,
    "Wheelchair": 0,
    "Windsurf": 0,
    "Workout": 7,
    "Yoga": 8
}

for obj in sa_jc:
    dt = obj["start_date"]
    id = obj["id"]
    dist = obj["distance"]
    elevation = obj["total_elevation_gain"]
    mt = obj["moving_time"]
    et = obj["elapsed_time"]
    sport_type = sport_type_enum[obj["sport_type"]]
    if sport_type == 0:
        print(obj["sport_type"])
    utc_offset = int(obj["utc_offset"])

    epoch_time = int(isoparse(dt).timestamp())
    data_items.append([epoch_time, id, dist, elevation, mt, et, sport_type, utc_offset])

data_items.sort()

for i in range(len(data_items)):
    data_items[i].insert(0,i+1)
    # print(datetime.datetime.fromtimestamp(data_items[i][1] + data_items[i][8]).strftime('%c'))
    # print(data_items[i])


datapath = "data/streams/"
files = listdir(datapath)

stream_types = ["time", "distance", "latlng", "altitude", "velocity_smooth", "heartrate", "cadence", "watts", "temp", "moving", "grade_smooth"]

for filename in files:
    id = int(filename.split(".")[0])

    data_index = -1
    for i in range(len(data_items)):
        if data_items[i][2] == id:
            data_index = i
            break
    if data_index == -1:
        print("data index not found")
        quit()

    rf = open(datapath + filename)
    jc = json.loads(rf.read())
    for st in stream_types:
        if st in jc:
            data_items[data_index].append(jc[st]["data"])
        else:
            data_items[data_index].append([])

    '''
    if "latlng" in jc and "altitude" in jc:
        # bf.write(struct.pack("@l", id))
        array_size = len(jc["latlng"]["data"])
        # bf.write(struct.pack("@l", array_size))
        for i in range(array_size):
            lat, lng = jc["latlng"]["data"][i]
            alt = jc["altitude"]["data"][i]
            bin = struct.pack("@fff", lat, lng, alt)
            # bf.write(bin)
    '''
    rf.close()

# data_items.append([epoch_time, id, dist, elevation, mt, et, sport_type, utc_offset])
bf = open("data/all.strava", "wb")
bf.write(bytes(".STRAVA", "ascii"))
bf.write(struct.pack("@l", 1))
bf.write(struct.pack("@l", len(data_items)))
for i in range(len(data_items)):
    print(i, end=" ")
    # internal id
    bf.write(struct.pack("@l", data_items[i][0]))
    # epoch_time
    bf.write(struct.pack("@l", data_items[i][1]))
    # Strava id
    bf.write(struct.pack("@l", data_items[i][2]))
    # distance
    bf.write(struct.pack("@f", data_items[i][3]))
    # elevation
    bf.write(struct.pack("@f", data_items[i][4]))
    # mt
    bf.write(struct.pack("@l", data_items[i][5]))
    # et
    bf.write(struct.pack("@l", data_items[i][6]))
    # sports_type
    bf.write(struct.pack("@B", data_items[i][7]))
    # utc offset
    bf.write(struct.pack("@l", data_items[i][8]))

    print(datetime.datetime.fromtimestamp(data_items[i][1] + data_items[i][8]).strftime('%c'))
    
    if len(data_items[i]) == 9:
        for j in range(len(stream_types)):
            bf.write(struct.pack("@l", 0))
    elif len(data_items[i]) == 20:
        stream_length = -1
        for j in range(len(stream_types)):
            bf.write(struct.pack("@l", len(data_items[i][9+j])))
            if len(data_items[i][9+j]) > 0:
                if stream_length == -1:
                    stream_length = len(data_items[i][9+j])
                elif stream_length != len(data_items[i][9+j]):
                    print("stream length not consitant")
                    quit()

                # time, int
                if j == 0:
                    for k in range(stream_length):
                        bf.write(struct.pack("@l", data_items[i][9+j][k]))
                # distance, float
                elif j == 1:
                    for k in range(stream_length):
                        bf.write(struct.pack("@f", data_items[i][9+j][k]))
                # latlng, [float, float]
                elif j == 2:
                    for k in range(stream_length):
                        bf.write(struct.pack("@ff", data_items[i][9+j][k][0], data_items[i][9+j][k][1]))
                # altitude, float
                elif j == 3:
                    for k in range(stream_length):
                        bf.write(struct.pack("@f", data_items[i][9+j][k]))
                # velocity_smooth, float
                elif j == 4:
                    for k in range(stream_length):
                        bf.write(struct.pack("@f", data_items[i][9+j][k]))
                # heartrate, int
                elif j == 5:
                    for k in range(stream_length):
                        bf.write(struct.pack("@l", data_items[i][9+j][k]))
                # cadence, int
                elif j == 6:
                    for k in range(stream_length):
                        bf.write(struct.pack("@l", data_items[i][9+j][k]))
                # watts, int
                elif j == 7:
                    for k in range(stream_length):
                        if data_items[i][9+j][k] == None:
                            bf.write(struct.pack("@l", 0))
                        else:
                            bf.write(struct.pack("@l", data_items[i][9+j][k]))

                # temp, int
                elif j == 8:
                    for k in range(stream_length):
                        bf.write(struct.pack("@l", data_items[i][9+j][k]))
                # moving, bool
                elif j == 9:
                    for k in range(stream_length):
                        bf.write(struct.pack("@?", data_items[i][9+j][k]))
                # smooth_grade, float
                elif j == 10:
                    for k in range(stream_length):
                        bf.write(struct.pack("@f", data_items[i][9+j][k]))
    else:
        print("len of data items not 9 or 20")
        quit()

bf.close()
