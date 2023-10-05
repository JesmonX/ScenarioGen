import csv
import pandas as pd
import numpy as np
from VehicleDef import Vehicle
path_meta = "./01_tracksMeta.csv"
path_rec = "./01_recordingMeta.csv"
path_trac = "./01_tracks.csv"
data_rec = pd.read_csv(path_rec)
data_meta_csv = csv.reader(open(path_meta))

vehicle_num = data_rec['numVehicles'][0]
vehicle_list = []

for row in data_meta_csv:  # extra
    if row[0].isdigit():  # skip the first
        vehicle_list.append(Vehicle(row[0], row[6], row[3], row[4]))

for i in range(10):
    v = vehicle_list[i]
    print(v.id, v.type, v.frame_init, v.frame_finish)



