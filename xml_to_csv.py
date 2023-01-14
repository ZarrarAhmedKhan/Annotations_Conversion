import os
import sys
import pandas as pd
from glob import glob
import xml.etree.ElementTree as ET


def xml_to_csv(annotation_path):
    xml_list = []
    # filenames = os.listdir(path + '/')
    # sorted_filenames = sorted(filenames, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    for xml_file in glob(f'{annotation_path}/*.xml'):
        # xml_file = annotation_path + '/' +  xml_file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text),
                     int(member[4][0].text) + int((int(member[4][2].text) - int(member[4][0].text))/2),
                     int(member[4][1].text) + int((int(member[4][3].text) - int(member[4][1].text))/2)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'bx', 'by']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    annotation_path = sys.argv[1]
    print (annotation_path)
    xml_df = xml_to_csv(annotation_path)
    xml_df.to_csv('shelfr_store_4.csv', index=None)
    print('Successfully converted xml to csv.')


if __name__ == '__main__':
    main()
