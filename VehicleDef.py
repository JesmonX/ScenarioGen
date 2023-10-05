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
