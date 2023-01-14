# ANNOTATION CONVERSION

## XML_to_CSV

* `annotation_folder_path = 'data/annotations'`

> `python3 xml_to_csv.py annotation_folder_path`

## CSV_to_TXT

* `csv_file_path = 'out.csv'`

* `save_dir = 'data/labels'`

> `python3 csv_to_txt.py csv_file_path save_dir`

### Output Files

* `class_name_to_id_mapping.txt`

* `save_dir containing all images annotations in txt format (yolo-format)`

## TXT_to_CSV

* `place your class_labels list`

* `test_folder_path containing "images_folder" and "labels_folder"`

> `python3 txt_to_csv.py test_folder_path`



