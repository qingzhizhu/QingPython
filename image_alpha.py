#!/usr/bin/python
#coding=utf-8
#desc:查找完全非带透明度图片，并设置一个像素带透明值
#author:gengkun123@gmail.com

import os,sys
import re
import numpy as np
import cv2

DIR=os.getcwd()
DIR_WORK = "/Users/kevin/elex/cod/cod_project2/Client/Unity/Assets/CustomAssets/Arts"
outStr=""

# img_path = DIR+"/img_test_red.png"
# img_path1 = DIR+"/img_test_red1.png"

# import numpy as np
# import cv2
# img = cv2.imread(img_path,  cv2.IMREAD_UNCHANGED)

# img_alpha = img[:,:,3]
# idmax = np.where(img_alpha != 255)
# # print(idmax[0])
# # print("长度")
# alpha_num = len(idmax[0])
# print(alpha_num)
# if(alpha_num < 1):
#     print("ok！")
#     img[0][0][3] = 120
#     cv2.imwrite(img_path1, img)


def CheckAlpha(imgPath):
    global outStr
    # print(imgPath)
    img = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)
    # print(img.shape)
    if(img.shape[2] < 4):
        # print("no alpha")
        return False
    img_alpha = img[:,:,3]
    idmax = np.where(img_alpha != 255)
    # print(idmax[0])
    # print("长度")
    alpha_num = len(idmax[0])
    # print(alpha_num)
    if(alpha_num < 1):
        # print("imgPaht:"+imgPath)
        outStr = outStr + imgPath + "\n"
        img[0][0][3] = 224
        cv2.imwrite(imgPath, img)
    return alpha_num < 1
        

regular = re.compile(r'^(.*)\.(jpeg|bmp|gif|png|JPEG|BMP|GIF|PNG|tif|TIF)$')
#regular = re.compile(r'^(.*)\.(tga)$')

picDic = {}

i=0
list_dirs = os.walk(DIR_WORK)
for root, dirs, files in list_dirs: 
    # print(root)
    # print(dirs)
    for f in files:
        picName = os.path.join(root, f)    #将分离的部分组成一个路径名
        # print(picName)
        if regular.match(picName):
            b = CheckAlpha(picName)
            if b:
                i+=1
                if(i>5):
                    print(outStr)
                    exit(0)



print(outStr)
print("Done!")