from csv import reader
from os import walk
from settings import *

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter = ",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surf_list = []
    for folder,subfolders,img_file in walk(path):
        for img in img_file:
            full_path = path+"/"+img
            imf_surf = pg.image.load(full_path).convert_alpha()
            surf_list.append(imf_surf)

    return surf_list


