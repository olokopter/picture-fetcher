import pickle
import numpy
import gzip
from PIL import Image
with open("save.p", 'rb') as fo:
    dictonary = pickle.load(fo, encoding='bytes')

pic_counter = 0
for item in dictonary["data"]:
     
    im = Image.new("RGB", (32, 32))
    pix = im.load()
    counter = 0
    for y in range(32):
        for x in range(32):
            
            pix[x,y] = (item[counter],item[counter+1024],item[counter+2*1024])
            counter+=1
    pic_counter+=1
    im.save("test"+str(pic_counter)+".png", "PNG")
    if pic_counter >5 :
        break
# print(dictonary)
