import json
import numpy as np
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os
# -----------------
# txt数据格式：path，xmin,ymin,xmax,ymax
# 每一行表示一个image
# --------------------

filename = 'instances_val2017.json'
f = open(filename,encoding='utf-8')
res = f.read()
data = json.loads(res)
# 数据集共90个类
# 保存数据的文件夹
folder = filename.split('.')[0]+'_txt'
if not os.path.exists(folder):
    os.mkdir(folder)

# 首先得到数据的categories的关键字
category = data['categories']
category_id ={}
for category_per in category:
    id = category_per['id']
    cls = category_per['name']
    category_id[id] = cls

print(category_id)
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
            # 根据图像ID，构建图像基本信息子目录
            # 图像路径
            image_path = imageID_all_info[imageID_per]['path']
            # 每一张图片信息写在txt文件
            # filename1 = imageID_all_info[imageID_per]['filename'].split('.')[0]
            file_write = folder + '/' + filename.split('.')[0] + '.txt'
            # 图像包含了多少个bounding box
            boundingBox_image = [j for j in data[images_attr] if j['image_id']==imageID_per]
            boundingBox_cord =''
            path_cord =''
            if len(boundingBox_image)==0:
                path_cord = image_path +'/n'
                with open(file_write, 'a+') as f:
                    f.write(path_cord)
                continue
            # 输出每张boundging box的坐标信息，以及所属类信息
            for boundingBox_per in boundingBox_image:
                # 添加boundingBox所属类的id
                id = boundingBox_per['category_id']
                # 位置信息转换，x,y,w,h转为xmin,ymin,xmax,ymax
                x = boundingBox_per['bbox'][0]
                y = boundingBox_per['bbox'][1]
                w = boundingBox_per['bbox'][2]
                h = boundingBox_per['bbox'][3]
                xmin = str(x)
                ymin = str(y)
                xmax= str(round(x+w,2))
                ymax=str(round(y+h,2))
                boundingBox_cord += xmin +','+ymin+','+xmax+','+ymax+','+str(id)+'  '

            boundingBox_cord = boundingBox_cord.rstrip()
            boundingBox_cord += '\n'
            path_cord = image_path + ' '+boundingBox_cord
            with open(file_write, 'a+') as f:
                f.write(path_cord)


