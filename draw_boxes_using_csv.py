import pandas as pd
import cv2
import sys

# get first frame of the video (third portion of the video)
def get_image(image_path):
	img = cv2.imread(image_path)
	return img

def draw_boxes_from_csv(csv_file_path, image_name):
	csv_file = pd.read_csv(csv_file_path)
	img = get_image(image_path)
	df = pd.DataFrame(csv_file)
	first_frame = df.loc[df['filename'] == image_name]
	print(first_frame)
	for index, row in first_frame.iterrows():
		print(row['xmin'], row['xmax'])
		x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
		cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
	cv2.imwrite("out.jpg", img)

if __name__ == '__main__':

	csv_file_path = sys.argv[1]
	image_path = sys.argv[2]

	image_name = image_path.split('/')[-1]
	draw_boxes_from_csv(csv_file_path, image_name)
