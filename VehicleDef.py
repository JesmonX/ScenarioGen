class Vehicle:
    id = 0
    type = 0
    frame_init = 0
    frame_finish = 0

    def __init__(self, id_num, type_str, init_num, finish_num):
        self.id = id_num
        self.type = type_str
        self.frame_init = init_num
        self.frame_finish = finish_num

def read_track(id,data):  # track data
    v_track = data[data['id'] == id]  # get the track of specific vehicle 
    v_track = v_track.reset_index(drop=True)  # reset the index
    return v_track
'''
class VehicleTrack:
    def __init__(self, id, frame, x, y, vx, vy, ax, ay, pid):
        self.id = id
        self.frame = frame
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.pid = pid
'''
