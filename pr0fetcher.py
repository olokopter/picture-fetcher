import pr0Api
from PIL import Image
import requests
from io import BytesIO
from resizeimage import resizeimage
import numpy as np
import pickle
import os

import time



THUMBURL = "http://thumb.pr0gramm.com/"
def main():
    lastID = None 
    startUp = True
    start_time = time.time()
    numberOfPictures = 0
    saveStr = "save"
    max_file_size = 1 #in MB 
    for iRedo in range(0,500):
        
        api = pr0Api.Api()
        api.enableNSFW()
        api.enableSFW()
        resultJSON = api.getAllFrom(startItemID=lastID)
        all_images = []
        test_counter = 0
        label = []
        lastID = resultJSON[-1]["promoted"]
#         print(lastID)
#         print(len(resultJSON))
        numberOfPictures+=len(resultJSON)
        print ("Fetching the next "+str(len(resultJSON)))
        for item in resultJSON:
    #         print(item)
            response = requests.get(THUMBURL+item["thumb"])
            img = Image.open(BytesIO(response.content))
            img = resizeimage.resize_cover(img, [32, 32], validate=False)
#             img.save(str(item["id"])+".jpeg", img.format)
            pixels = img.load()
            all_array = []
            redPixels= []
            greenPixels = []
            bluePixels =[]
            
            labelFlag = 0
            if item["flags"] ==2:
                labelFlag = 1
            else:
                labelFlag = 0
            for iCol in range(0,32):
                
                for iRow in range(0,32):
                    redPixels.append((pixels[iRow, iCol][0]))
                    greenPixels.append((pixels[iRow, iCol][1]))
                    bluePixels.append((pixels[iRow, iCol][2]))
            label.append(labelFlag)
            all_array.extend(redPixels)
            all_array.extend(greenPixels)
            all_array.extend(bluePixels)
            all_images.append(all_array)
            test_counter+=1
#             if test_counter>10:
#                 break
        print ("Fetched",numberOfPictures,"in total")
        print("--- %s needed seconds ---" % (time.time() - start_time))

        np_imgarray = np.array(all_images,dtype=np.uint8)
        np_label = np.array(label,dtype=np.uint8)
        dump_dict = {"data":np_imgarray,"labels":np_label}
        
        
        if startUp:
            pickle.dump( dump_dict, open( saveStr+".p", "wb" ) )
            startUp=False
        else:
            pickle.dump( dump_dict, open( saveStr+".p", "ab" ) )
        statinfo = os.stat(saveStr+".p")
        
        file_size = statinfo.st_size/300e+6
        print ("filesize",file_size)
        if file_size > max_file_size :
            saveStr = saveStr+str(iRedo)
            print("Filesize larger than ",max_file_size,"starting new file: ",saveStr)
            
            startUp=True
#         input("next")
    
#     print(resultJSON)
if __name__ == "__main__":
    main()