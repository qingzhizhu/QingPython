#!/usr/bin/python
# coding=utf-8
# desc:
# author:gengkun123@gmail.com

import os
import sys
import re
# import matplotlib.pyplot as plt # plt 用于显示图片
# import matplotlib.image as mpimg # mpimg 用于读取图片
import cv2
import numpy as np


userDir=""

if __name__ == "__main__":
    # for arg in sys.argv:
    # 	print(arg)

    fullName = sys.argv[0]
    print("脚本名：", fullName)
    if fullName[0] == '/':
        print('切换目录')
        os.chdir(os.path.abspath(os.path.dirname(fullName)))

    for i in range(1, len(sys.argv)):
        print("参数", i, sys.argv[i])

    if len(sys.argv) > 1:
        userDir = sys.argv[1]

DIR = os.getcwd()
DIR_WORK = DIR+"/../../Client/Unity/Assets/CustomAssets/Arts/UiAssets"
# Client/Unity/Assets/CustomAssets/Arts/UiAssets/
if userDir != "":
    DIR_WORK = userDir
print(DIR_WORK)


regular = re.compile(
    r'^(.*)\.(bmp|gif|png|JPG|JPEG|BMP|GIF|PNG|tif|TIF)$')
# regular = re.compile(r'^(.*)\.(tga)$')



outStr = ""
i = 0
list_dirs = os.walk(DIR_WORK)
for root, dirs, files in list_dirs:
    # print(root)
    # print(dirs)

    for f in files:
        picName = os.path.join(root, f)  # 将分离的部分组成一个路径名
        if regular.match(picName):
            # fileSize = os.path.getsize(picName)
            # print(picName)
            img =  cv2.imread(picName, cv2.IMREAD_UNCHANGED) 
            if(img.shape[2] < 4):
                continue
            img_alpha = img[:,:,3]
            # print(img_alpha)
            idxs_alpha = np.where(img_alpha != 255)
            # print(idxs_alpha)
            # print(len(idxs_alpha[0]))
            len_noalpha = len(idxs_alpha[0])
            if len_noalpha < 1:
                print("完全不透明的图的一个像素变成微透:%s" % picName)
                outStr += picName + "\n"
                img[0][0][3] = 254 
                cv2.imwrite(picName, img)
                # sys.exit(0)\

                

    # 	if i>10:
    # 		break
    # if i>10:
    # 	break

print(outStr)

# 写入文件
writeFilePath = DIR+"/log_alphaPic.txt"
if os.path.exists(writeFilePath):
    os.remove(writeFilePath)

file_object = open(writeFilePath, 'w')
file_object.write(outStr)
file_object.close()

if outStr.strip() != "":
    sys.exit(1)

print("Done!")
