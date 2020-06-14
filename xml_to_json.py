# xml to json转换
import json
import os
from xml.dom import minidom

def xml_to_json(folder):
    mydict = {}
    # 列出某个文件夹的xml文件
    # folder = 'instances_val2017_xml'
    file_all = os.listdir(folder)
    file_xml_all = [file for file in file_all if '.xml' in file[-4:]]
    file_path = folder + '/' + file_xml_all[0]
    # 读其中某一个xml文件，所有xml文件共同的属性
    dom = minidom.parse(file_path)
    # 得到文档元素对象
    root = dom.documentElement
    # 获取子标签
    data_base = root.getElementsByTagName('database')[0].firstChild.data
    # root.
    xml_path = root.getElementsByTagName('path')[0].firstChild.data
    data_path = xml_path[0:xml_path.find('.org')+4]
    # info属性
    info_attr = {}
    info_attr['description'] = data_base
    info_attr['url'] = data_path
    # license属性
    license_attr = {}
    license_attr['name'] ='non-commercial license'
    # 读所有xml文件
    # images属性
    images_attr_list = []
    images_attr = {}
    # annotations属性
    annotations_attr_list = []
    annotations_attr = {}
    # categories属性
    categories_id = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck'
        , 9: 'boat', 10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird'
        , 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra'
        , 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase'
        , 34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard'
        , 42: 'surfboard', 43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
    categories_attr_list = []
    categories_attr = {}
    for file_xml_per in file_xml_all:
        file_path = folder + '/' + file_xml_per
        try:
            dom = minidom.parse(file_path)
        except:
            continue

        root = dom.documentElement
        # imageID属性
        image_id = root.getElementsByTagName('ImageID')[0].firstChild.data
        print('----------\n',image_id)
        images_attr['id'] = image_id
        # imagePath属性
        image_path = root.getElementsByTagName('path')[0].firstChild.data
        images_attr['path'] = image_path
        # imageName属性
        image_name = root.getElementsByTagName('filename')[0].firstChild.data
        images_attr['path'] = image_name
        # imageSize属性
        image_size_node = root.getElementsByTagName('size')[0]
        images_attr['width'] = image_size_node.getElementsByTagName('width')[0].firstChild.data
        images_attr['height'] = image_size_node.getElementsByTagName('height')[0].firstChild.data
        # 添加到列表
        images_attr_list.append(images_attr)
        # 对每一个xml所包含的boundingBox写到annotations
        object_node_all = root.getElementsByTagName('object')
        for object_node_per in object_node_all:
            bndbox_node = object_node_per.getElementsByTagName('bndbox')[0]
            xmin = bndbox_node.getElementsByTagName('xmin')[0].firstChild.data
            ymin = bndbox_node.getElementsByTagName('ymin')[0].firstChild.data
            xmax = bndbox_node.getElementsByTagName('xmax')[0].firstChild.data
            ymax = bndbox_node.getElementsByTagName('ymax')[0].firstChild.data
            x = float(xmin)
            y = float(ymin)
            w = round(float(xmax) - float(xmin),2)
            h = round(float(ymax) - float(ymin),2)
            coord_list = [x,y,w,h]
            annotations_attr['bbox'] = coord_list
            #框所属id
            annotations_attr['category_id'] = object_node_per.getElementsByTagName('classID')[0].firstChild.data
            # imageID
            annotations_attr['image_id'] = image_id
            # 添加到列表
            annotations_attr_list.append(annotations_attr)
    # categories属性
    for key1 in categories_id.keys():
        categories_attr[key1] = categories_id[key1]
        categories_attr_list.append(categories_attr)

    # 所有字典结合起来
    mydict['info'] = info_attr
    mydict['licenses'] = license_attr
    mydict['images'] = images_attr_list
    mydict['annotations'] = annotations_attr_list
    mydict['categories'] = categories_attr_list
    # 写入json文件
    with open('xml_to_js.json','w') as f:
        json.dump(mydict,f)
        print('loaded finish')
    return mydict

if __name__ == '__main__':
    folder = 'instances_val2017_xml'
    xml_to_json(folder)
