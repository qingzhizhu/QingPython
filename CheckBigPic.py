#!/usr/bin/python
#coding=utf-8
#desc:查找出较大图片
#author:gengkun123@gmail.com

import os,sys
import re
from PIL import Image


DIR=os.getcwd()

DIR_WORK="/Users/kevin/elex/cod/cod_project2/Client/Unity/Assets/CustomAssets/Arts"

#50MB
MAXSIZE=52428800
MULTIPLE=1.05

if __name__ == "__main__":
	# for arg in sys.argv:  
	# 	print(arg)

	print ("脚本名：", sys.argv[0])
	for i in range(1, len(sys.argv)):
		print("参数", i, sys.argv[i])

	if len(sys.argv) > 1:
		p1=float(sys.argv[1])
		if p1 < 1.05:
			p1 = 1.05
		MULTIPLE=p1
		print("倍数:"+str(MULTIPLE))

# sys.exit(0)

regular = re.compile(r'^(.*)\.(jpg|jpeg|bmp|gif|png|JPG|JPEG|BMP|GIF|PNG|tif|tga|TIF)$')
#regular = re.compile(r'^(.*)\.(tga)$')

def getMemorySize(wei, hei, sizePrePixel):
	return wei*hei*sizePrePixel

print("检查较大图片！文件大于50M或者阈值大于%d%%可以优化图片大小." %(MULTIPLE*100))

picDic = {}
outStr=""
i=0
list_dirs = os.walk(DIR_WORK)
for root, dirs, files in list_dirs: 
	#print(root)
	# print(dirs)

    for f in files:
    	picName = os.path.join(root, f)    #将分离的部分组成一个路径名
    	if regular.match(picName):
    		fileSize=os.path.getsize(picName)
    		if fileSize < 1024:
    			continue
    			
    		if fileSize > MAXSIZE:
    			# print("%s\t大于50M!!!请检查! 文件:%dMB " %(picName, fileSize/1048576))
    			outStr=outStr+"%s\t大于50M!!!请检查! 文件:%dMB " %(picName, fileSize/1048576) + "\n"
    			continue
    		im = Image.open(picName, "r")
    		width, height = im.size
    		#print(width, height)
    		
    		memSize=getMemorySize(width, height, 4)
    		if fileSize >= memSize*MULTIPLE:
    			i=i+1
    			picDic[picName]={"threshold":int(100.0*fileSize/memSize), "width":width, "height":height, "fileSize":fileSize, "memorySize":memSize}
    		
    # 	if i>10:
    # 		break
    # if i>10:
    # 	break

# sort=sorted(picDic.items(),key=lambda e:e[1]["fileSize"],reverse=True)   #排序
sort=sorted(picDic.items(),key=lambda e:e[1]["threshold"],reverse=True)   #排序
for item in sort:
	# print("阈值:%d;\t%s;\t(wid=%d,hei=%d);\tfileSize:%dKB;\tmemorySize:%dKB;" % (item[1]["threshold"], item[0], item[1]["width"], item[1]["height"], item[1]["fileSize"]/1024, item[1]["memorySize"]/1024))
	outStr = outStr + "阈值:%d%%;\t%s;\t(wid=%d,hei=%d);\tfileSize:%dKB;\tmemorySize:%dKB;" % (item[1]["threshold"], item[0], item[1]["width"], item[1]["height"], item[1]["fileSize"]/1024, item[1]["memorySize"]/1024) + "\n"

print(outStr)

#写入文件
writeFilePath = DIR+"/log_bigPic.txt"
if os.path.exists(writeFilePath):
     os.remove(writeFilePath)

if outStr != "":
    file_object = open(writeFilePath, 'w')
    file_object.write(outStr)
    file_object.close()
    sys.exit(1)
    print("检查有较大图片！")

print("Done!")
