import os
import pathlib

from Postables.meme_selector import MemeFolder

folder_contents = os.listdir(pathlib.Path(__file__).parent.resolve())
folders_only = []
for file in folder_contents:
    if '.' in str(file):
        pass
    else:
        folders_only.append(file)
