import pandas as pd
import cv2
import sys

# get first frame of the video (third portion of the video)
def get_first_frame_of_the_video():
	# cap = cv2.VideoCapture("out_2min_stitched_20220106-ct-girls-field-2-game-3.mp4")

	# cap.set(1,1)
	# ret, img = cap.read()
	# img = img[:, int(img.shape[1]) - int(img.shape[1]/3):]
	# cv2.imwrite("m_1.jpg", img)
	# cap.release()

	img = cv2.imread('test_predictions_yolo/images/0_64_IMG_20221108_132423.jpg')
	return img

def draw_boxes_from_csv(im):
	csv_file = pd.read_csv(sys.argv[1])
	df = pd.DataFrame(csv_file)
	first_frame = df.loc[df['filename'] == '0_64_IMG_20221108_132423.jpg']
	print(first_frame)
	for index, row in first_frame.iterrows():
		print(row['xmin'], row['xmax'])
		x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
		cv2.rectangle(im,(x1,y1),(x2,y2),(0,255,0),2)
	cv2.imwrite("m_1.jpg", im)

if __name__ == '__main__':
	first_f = get_first_frame_of_the_video()
	draw_boxes_from_csv(first_f)
