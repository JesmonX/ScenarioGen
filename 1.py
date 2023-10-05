import csv
import pandas as pd
import numpy as np
path_meta = "./02_tracksMeta.csv"
path_rec = "./01_recordingMeta.csv"
path_trac = "./01_tracks.csv"
data_meta_csv = csv.reader(open(path_meta))
# data_meta = pd.read_csv(path_meta)
meanXVelocity = data_meta['meanXVelocity']
vehicle_id = data_meta['id']
print("meanXVelocity.min : ", meanXVelocity.min())


with open("02_newMeta", "a", encoding="utf-8", newline="") as f:
    csv_writer = csv.writer(f)
    n = 0
    for row in data_meta_csv:
        if n == 0 and row[0] != 1: # skip the first time
            next(data_meta_csv)
        # print(vehicle_id[n],row)

        if meanXVelocity[vehicle_id[n]-1] <= 20:
            print("find one")
            csv_writer.writerow(row)
        n += 1

csv_reader = csv.reader(open("02_newMeta"))
n = 0
for row in csv_reader:
    print(n, " ", row)
    n += 1
    if n > 100:
        break


