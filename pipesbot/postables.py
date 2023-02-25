import pathlib
import os

postables_folders_only = []

def mac_or_windows():
    main_directory = str(pathlib.Path(__file__).parent.resolve())
    if '/' in main_directory:
        return 'MAC'
    else:
        return 'WIN'

def postables_pathfinder():
    if mac_or_windows() == 'MAC':
        return os.listdir(str(pathlib.Path(__file__).parent.resolve()) + '/postable_content')
    else:
        return os.listdir(str(pathlib.Path(__file__).parent.resolve()) + '\\postable_content')

def return_postables_folders():
    postables_folders_only = []
    for file in postables_pathfinder():
        if '.' in str(file):
            pass
        else:
            postables_folders_only.append(file)
    return postables_folders_only