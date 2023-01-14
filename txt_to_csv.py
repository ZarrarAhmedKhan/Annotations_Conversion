import cv2
import os
import pandas as pd
from glob import glob
import sys

# test folder containg "images folder" and label folder
test_folder = sys.argv[1]

class_labels = ['person', 'ball']

df = pd.DataFrame(columns=['filename','width','height','xmin','ymin','xmax','ymax','confidence','class_name'])

def check_image(txt_file, images_list):

	txt_file_name = txt_file.split('/')[-1].split('.txt')[0] + '.jpg'
	print("image_file_name:" , txt_file_name)
	if txt_file_name in images_list:
		# print("Image present")
		image = cv2.imread(f"{test_folder}/images/{txt_file_name}")
		ht, wd,_ = image.shape
		return [ht,wd, txt_file_name]
	else:
		print("image not present")
		return False


def get_all_information(yolo_box, image_height,image_width):

	try:
		class_number = int(yolo_box[0])
		class_name = class_labels[class_number]
		x_yolo = float(yolo_box[1])
		y_yolo = float(yolo_box[2])
		yolo_width = float(yolo_box[3])
		yolo_height = float(yolo_box[4])
		yolo_confidence = float(yolo_box[5])
	except IndexError:
		yolo_confidence = None

	# Convert Yolo Format to csv
	box_width = yolo_width * image_width
	box_height = yolo_height * image_height
	x_min = str(int(x_yolo * image_width - (box_width / 2)))
	y_min = str(int(y_yolo * image_height - (box_height / 2)))
	x_max = str(int(x_yolo * image_width + (box_width / 2)))
	y_max = str(int(y_yolo * image_height + (box_height / 2)))

	print(class_name, x_min, y_min, x_max , y_max)
	return [class_name, x_min, y_min, x_max , y_max, yolo_confidence]


images_list = os.listdir(f'{test_folder}/images')
print(images_list)
for txt_file in glob(f'{test_folder}/labels/*'):
	print(txt_file)
	check = check_image(txt_file, images_list)
	if not check:
		break
	else:
		ht,wd,image_file_name = check[0], check[1], check[2]
		print(ht,wd)
	file = open(txt_file, 'r')
	Lines = file.readlines()

	for line in Lines:
		line = line.strip()
		print("line: ", line)
		split_line = line.split(' ')
		print(split_line)
		bounding_box_list = get_all_information(split_line, ht,wd)
		df = df.append({'filename':image_file_name,'width':wd,'height':ht,'xmin':bounding_box_list[1],'ymin':bounding_box_list[2],'xmax':bounding_box_list[3],'ymax':bounding_box_list[4],'confidence':bounding_box_list[5],'class_name':bounding_box_list[0]},ignore_index=True)
		# break
	# break

df.to_csv('output' + '.csv')

