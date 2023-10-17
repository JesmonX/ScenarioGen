import csv
import pandas as pd
import os
import glob
# import numpy as np
path = 'D:/MyClasses/mus/highd-dataset-v1.0/data'
import VehicleDef as vd

for file_num in range(1, 60):
    print("begin : brake{}".format(file_num))
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

    for file in glob.glob('brake_scenario//{:0>2d}//*'.format(file_num)):
        os.remove(file)
    for track in track_list:  # for every track(vehicle)
        # ego vehicle should be almost at a constant speed

        pre_vehicle_list = []
        for v in track['precedingId']:
            if v != 0 and v not in pre_vehicle_list:
                pre_vehicle_list.append(v)

        if not pre_vehicle_list:  # no preceding vehicle
            continue

        # print(pre_vehicle_list)
        # now we have the pre_vehicle_list
        # for every pre_vehicle, we need to find if it is braking

        '''
        get its pre_vehicle_list
        for every pre_vehicle
            find if its a is larger than 2 at its speed direction
                if so, find if the frame is in the range of the track of ego vehicle
                    if so , extract the track of ego vehicle and pre_vehicle and write to the file as a scenario
        '''

        for pre_vehicle in pre_vehicle_list:
            pre_track = track_list[pre_vehicle]
            # if ego vehicle is not at a constant speed in the range of its preceding car is pre_vehicle

            for i in range(len(pre_track['frame'])):  # for every frame until we find the scenario
                if ((pre_track['xAcceleration'][i] >= 2 and pre_track['xVelocity'][i]) < 0 or
                        (pre_track['xAcceleration'][i] <= -2 and pre_track['xVelocity'][i] > 0)) :
                    if pre_track['frame'][i] in range(track['frame'][0], track['frame'][len(track['frame']) - 1]):
                        # if at the beginning of brake, the ego is at a constant speed
                        frame_value = pre_track['frame'][i]
                        selected_rows = track.query("`precedingId` == @pre_vehicle and `frame` <= @frame_value")
                        xAcceleration_values = selected_rows['xAcceleration']
                        if xAcceleration_values.max() > 0.1 or xAcceleration_values.min() < -0.1:
                            break
                        # brake and in the range
                        data_frame = track
                        data_frame.to_csv("brake_scenario//{:0>2d}//brake{:0>2d}_ego.csv".format(file_num,brake_file_num),
                                          index=False, sep=',', mode='w')
                        data_frame = pre_track
                        data_frame.to_csv("brake_scenario//{:0>2d}//brake{:0>2d}_pre.csv".format(file_num,brake_file_num),
                                          index=False, sep=',', mode='w')
                        brake_file_num = brake_file_num + 1
                        break
                    # we find the scenario
                    # we need to extract the track of ego vehicle and pre_vehicle

                    # if we find ,then we go to the next pre_vehicle