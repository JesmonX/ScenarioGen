import csv
import pandas as pd
import os
import glob
# import numpy as np
# path = 'D:/MyClasses/mus/highd-dataset-v1.0/data'
path = '.'
import VehicleDef as vd

file_num = 1
path_meta = "{}/{:0>2d}_tracksMeta.csv".format(path, file_num)
path_rec = "{}/{:0>2d}_recordingMeta.csv".format(path, file_num)
path_trac = "{}/{:0>2d}_tracks.csv".format(path, file_num)
# frame,id,x,y,width,height,xVelocity,yVelocity,xAcceleration,yAcceleration,frontSightDistance,backSightDistance,dhw,thw,ttc,precedingXVelocity,precedingId,followingId,leftPrecedingId,leftAlongsideId,leftFollowingId,rightPrecedingId,rightAlongsideId,rightFollowingId,laneId
data_rec = pd.read_csv(path_rec)
data_meta_csv = csv.reader(open(path_meta))
data_trac = pd.read_csv(path_trac)
vehicle_num = data_rec['numVehicles'][0]

vehicle_list = []
for row in data_meta_csv:  # extra
    if row[0].isdigit():  # skip the first
        vehicle_list.append(vd.Vehicle(row[0], row[6], row[3], row[4]))
# begin to find the scenario
# for every track
brake_file_num = 1
track_list = []
for i in range(vehicle_num):
    track_list.append(vd.read_track(i, data_trac))
# now we have the track_list
# we can find the brake scenario
# we need to build a new file to store the brake scenario

# for track in track_list:  # for every track(vehicle)

print(len(track_list[1]))


    
    
    
    








