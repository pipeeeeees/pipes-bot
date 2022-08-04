import os
import random

class MemeFolder:
    def __init__(self, folder_name):
        self.name = folder_name
        self.self_list = os.listdir(os.getcwd() + '\\' + folder_name)
        self.self_list_len = len(self.self_list)
        self.index = 0
        random.shuffle(self.self_list)
        
    def return_path(self):
        if self.index >= self.self_list_len:
            self.index = 0
            random.shuffle(self.self_list)
        path_return = os.getcwd() + '\\' + self.name + '\\' + self.self_list[self.index]
        self.index += 1
        #print(path_return)
        return path_return
    
Obama = MemeFolder('obama')
Biden = MemeFolder('biden')
Brady = MemeFolder('brady')
Lebron = MemeFolder('lebron')
