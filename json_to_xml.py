import json
import numpy as np
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os

filename = 'instances_val2017.json'
with open(filename,'r',encoding='utf-8') as f:
    f1 = f.read()
    data = json.loads(f1)
# 数据集共90个类
# 保存数据的文件夹
folder = filename.split('.')[0]+'_xml'
if not os.path.exists(folder):
    os.mkdir(folder)

common_dict = {}
common_dict['folder'] = folder
common_dict['database'] = data['info']['description']

# 首先建立root
bases = Element('annotation')
# 建立一级根目录，所有xml文件都具有相同的key
for key,value in common_dict.items():
    SubElement(bases,key).text = value

# 打印并写xml文件
# xml = tostring(bases)
# dom = parseString(xml)
# print(dom.toprettyxml(' '))
# with open('test0.xml', 'w') as f:
#     dom.writexml(f, '',addindent='\t', newl='\n', encoding='utf-8')

# 首先得到数据的categories的关键字
category = data['categories']
category_id ={}
for category_per in category:
    id = category_per['id']
    cls = category_per['name']
    category_id[id] = cls


# 开始遍历字典，对每一个图像生成xml文件
imageID_all =[]
imageID_all_info = {}
for images_attr in list(data.keys()):
    if  images_attr == 'images':
        # 遍历每一个图像
        for data_per in data[images_attr]:
            # 获取图像名字
            image_name = data_per['file_name']
            # 获取图像路径
            image_route = data_per['coco_url']
            # 获取图像的像素和ID
            image_width = data_per['width']
            image_height = data_per['height']
            image_id = data_per['id']
            imageID_all.append(image_id)
            imageID_all_info[image_id]={'width':image_width,'height':image_height,'path':image_route,'filename':image_name}

    elif images_attr == 'annotations':
        # 根据id遍历每张图像的bounding box
        for imageID_per in imageID_all:
            print(imageID_per)
            if imageID_per ==148730:
                sss=1
            # 根据图像ID，构建图像基本信息子目录
            # 写一级目录，图像名字
            filename_node = SubElement(bases, 'filename')
            filename_node.text = imageID_all_info[imageID_per]['filename']
            # 添加图像ID子目录
            ImageID_node = SubElement(bases, 'ImageID')
            ImageID_node.text = str(imageID_per)
            # 写一级目录，图像路径
            path_node = SubElement(bases, 'path')
            path_node.text = imageID_all_info[imageID_per]['path']
            # 写一级目录，图像像素
            size = SubElement(bases, 'size')
            # 图像像素子目录
            SubElement(size, 'width').text = str(imageID_all_info[imageID_per]['width'])
            SubElement(size, 'height').text = str(imageID_all_info[imageID_per]['height'])
            boundingBox_image = [j for j in data[images_attr] if j['image_id']==imageID_per]
            # bounding box个数子目录
            boundingBox_num_node = SubElement(bases,'bboxNum')
            boundingBox_num_node.text = str(len(boundingBox_image))
            if len(boundingBox_image)==0:
                bases.remove(filename_node)
                bases.remove(ImageID_node)
                bases.remove(path_node)
                bases.remove(size)
                bases.remove(boundingBox_num_node)
                # bases.remove(object_node)
                continue
            # 输出每张boundging box的坐标信息，以及所属类信息
            for boundingBox_per in boundingBox_image:
                object_node = SubElement(bases, 'object')
                # 添加boundingBox所属类的目录
                id = boundingBox_per['category_id']
                cls = category_id[id]
                # 添加所属类的ID
                SubElement(object_node, 'classID').text = str(id)
                SubElement(object_node, 'name').text = str(cls)
                bndbox = SubElement(object_node,'bndbox')
                # 位置信息转换，x,y,w,h转为xmin,ymin,xmax,ymax
                x = boundingBox_per['bbox'][0]
                y = boundingBox_per['bbox'][1]
                w = boundingBox_per['bbox'][2]
                h = boundingBox_per['bbox'][3]
                xmin = x
                ymin = y
                xmax= round(x+w,2)
                ymax=round(y+h,2)
                SubElement(bndbox,'xmin').text = str(xmin)
                SubElement(bndbox,'ymin').text = str(ymin)
                SubElement(bndbox, 'xmax').text = str(xmax)
                SubElement(bndbox, 'ymax').text = str(ymax)

                # 每一个boundingbox写在xml文件
            file_write = folder + '/' + filename_node.text.split('.')[0] + '.xml'
            xml = tostring(bases)
            dom = parseString(xml)
                # print(dom.toprettyxml(' '))
            with open(file_write, 'w') as f:
                dom.writexml(f, '', addindent='\t', newl='\n', encoding='utf-8')

            # 删除图像的节点
            bases.remove(filename_node)
            bases.remove(ImageID_node)
            bases.remove(path_node)
            bases.remove(size)
            bases.remove(boundingBox_num_node)
            # 删除object
            object_all = bases.findall('object')
            for object_per in object_all:
                bases.remove(object_per)


# 打印并写xml文件
# xml = tostring(bases)
# dom = parseString(xml)
# print(dom.toprettyxml(' '))
print('hello')