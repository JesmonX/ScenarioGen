import csv
import pandas as pd
import os
import glob
# import numpy as np
path = 'D:/MyClasses/mus/highd-dataset-v1.0/data'
import VehicleDef as vd

for file_num in range(1, 60):
    print("begin : cut-in{}".format(file_num))
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
    cutin_file_num = 1
    track_list = []
    for i in range(vehicle_num):
        track_list.append(vd.read_track(i, data_trac))

    # now we have the track_list
    # we can find the cut-in scenario
    # we need to build a new file to store thecut scenario

    for file in glob.glob('cut-in_scenario//{:0>2d}//*'.format(file_num)):
        os.remove(file)
    
    for track in track_list:  # for every track(vehicle)

        # print(pre_vehicle_list)
        # now we have the pre_vehicle_list
        # for every pre_vehicle, we need to find if it is braking

        '''
        for every car 
            find if it changes lane(can just compare the 1st and last frame)
                if so, find the key frame and give its following car id after its changing;
                find if the car is at const speed    
        '''
        if len(track) == 0:  # no track 
            continue
        
        if track['laneId'][0] != track['laneId'][len(track)-1]:  # change lane
            key_frame = 0
            for i in range(len(track)):
                if track['laneId'][i] != track['laneId'][0]:
                    key_frame = i
                    break
            if (track['followingId'][key_frame] == track['followingId'][len(track)-1] and
                    track['followingId'][key_frame] != 0 and  # the following car exists
                    (key_frame - len(track))>10 and abs(key_frame) > 10):  # the key frame is not at the first or last

                following_vehicle = track['followingId'][key_frame]  # the following car id
                frame_value = track['frame'][key_frame]         # the key frame value
                selected_rows = track_list[following_vehicle].query("`frame` <= @frame_value")
                xAcceleration_values = selected_rows['xAcceleration']
                if xAcceleration_values.max() > 0.1 or xAcceleration_values.min() < -0.1:
                    continue
                
                data_frame = track
                data_frame.to_csv("cut-in_scenario//{:0>2d}//cut-in{:0>2d}_pre.csv".format(file_num,cutin_file_num),
                                  index=False, sep=',', mode='w')
                data_frame = track_list[following_vehicle]
                data_frame.to_csv("cut-in_scenario//{:0>2d}//cut-in{:0>2d}_ego.csv".format(file_num,cutin_file_num),
                                  index=False, sep=',', mode='w')
                cutin_file_num = cutin_file_num + 1
                continue
                
            






        



