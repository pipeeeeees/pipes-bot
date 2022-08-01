import os
import random

class MemeFolder:
    CURRENT_WORKING_DIR = os.getcwd()
    def __init__(self, folder_name):
        self.self_list = os.listdir(CURRENT_WORKING_DIR + '\\' + folder_name)
        self.self_list_len = len(self.self_list)
        self.index = 0
        random.shuffle(self.self_list)
        
    def return_path(self):
        path_return = CURRENT_WORKING_DIR + '\\' + self.self_list[self.index]
        self.index += 1
        print(path_return)
        return path_return
    
Obama = MemeFolder('obama')
Biden = MemeFolder('biden')
Brady = MemeFolder('brady')
Lebron = MemeFolder('lebron')
