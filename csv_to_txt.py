import os 
import random
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import json

random.seed(108)

# print(extract_info_from_xml('annotations/road4.xml'))

# Dictionary that maps class names to IDs
# class_name_to_id_mapping = {"trafficlight": 0,
#                            "stop": 1,
#                            "speedlimit": 2,
#                            "crosswalk": 3}
# class_name_to_id_mapping = {"ball": 0}

# Dictionary that maps class names to IDs
def func_class_name_to_id_mapping(dataframe, csv_file, save=True):
    class_counter = 0
    class_name_to_id_mapping = {}
    for i, ann in enumerate(dataframe.iterrows()):
        if ann[1]['class'] not in class_name_to_id_mapping:
            class_name_to_id_mapping[ann[1]['class']] = class_counter
            class_counter += 1
    print(class_name_to_id_mapping)
    if save:
        csv_file_name = csv_file.split('/')[-1]
        with open(f"{csv_file_name.split('.')[0]}_class_name_to_id_mapping.txt", 'w') as file:
            file.write(json.dumps(class_name_to_id_mapping, indent=4))
    return class_name_to_id_mapping



# Convert the info dict to the required yolo format and write it to disk
def convert_to_yolov5(info_dict, save_dir):
    print_buffer = []
    
    # For each bounding box
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
        
        # Transform the bbox co-ordinates as per the format required by YOLO v5
        b_center_x = (b["xmin"] + b["xmax"]) / 2 
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width    = (b["xmax"] - b["xmin"])
        b_height   = (b["ymax"] - b["ymin"])
        
        # Normalise the co-ordinates by the dimensions of the image
        image_w, image_h, image_c = info_dict["image_size"]  
        b_center_x /= image_w 
        b_center_y /= image_h 
        b_width    /= image_w 
        b_height   /= image_h 
        
        #Write the bbox details to the file 
        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
        
    img_extension = info_dict["filename"].split('.')[-1]
    
    # Name of the file which we have to save 
    save_file_name = os.path.join(save_dir, info_dict["filename"].replace(img_extension, "txt"))
    # print("-----")
    # Save the annotation to disk
    print("\n".join(print_buffer), file= open(save_file_name, "a"))

# Function to get the data from CSV Annotation File
def extract_info_from_csv(row):
    main_dict = {}
    main_dict['bboxes'] = []
    bbox = {}
    # print(row['class'])
    bbox['class'] = row['class']
    bbox['xmin'] = int(row['xmin'])
    bbox['ymin'] = int(row['ymin'])
    bbox['xmax'] = int(row['xmax'])
    bbox['ymax'] = int(row['ymax'])
    main_dict['bboxes'].append(bbox)
    main_dict['filename'] = row['filename']
    image_size = []
    image_size.append(int(row['width']))
    image_size.append(int(row['height']))
    image_size.append(3)
    main_dict['image_size'] = tuple(image_size)
    return main_dict



 # Get the annotations
csv_file = sys.argv[1]
save_dir = sys.argv[2]

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
annotations = pd.read_csv(csv_file)
dataframe = pd.DataFrame(annotations)

class_name_to_id_mapping = func_class_name_to_id_mapping(dataframe, csv_file)

# Convert and save the annotations
for i, ann in tqdm(enumerate(dataframe.iterrows())):
    print(i)
    # print(ann)
    info_dict = extract_info_from_csv(ann[1])
    print(info_dict)
    convert_to_yolov5(info_dict, save_dir)

# print("number of unique txt files: ", len(unique_files))