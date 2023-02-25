import os
import random
import pathlib

class MemeFolder:
    def __init__(self, folder_name):
        self.name = folder_name
        if '/' in str(pathlib.Path(__file__).parent.resolve()):
            self.self_list = os.listdir(str(pathlib.Path(__file__).parent.resolve()) + '/' + folder_name)
        else:
            self.self_list = os.listdir(str(pathlib.Path(__file__).parent.resolve()) + '\\' + folder_name)
        self.self_list_len = len(self.self_list)
        self.index = 0
        random.shuffle(self.self_list)
        
    def return_path(self):
        if self.index >= self.self_list_len:
            self.index = 0
            random.shuffle(self.self_list)
        if '/' in str(pathlib.Path(__file__).parent.resolve()):
            path_return = str(pathlib.Path(__file__).parent.resolve()) + '/' + self.name + '/' + self.self_list[self.index]
        else:
            path_return = str(pathlib.Path(__file__).parent.resolve()) + '\\' + self.name + '\\' + self.self_list[self.index]
        self.index += 1
        #print(path_return)
        return path_return