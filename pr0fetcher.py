import pr0Api
from PIL import Image
import requests
from io import BytesIO
from resizeimage import resizeimage
import numpy as np
import pickle
THUMBURL = "http://thumb.pr0gramm.com/"
def main():
    lastID = None 
    for iRedo in range(0,5):
        api = pr0Api.Api()
        api.enableNSFW()
        api.enableSFW()
        resultJSON = api.getAllFrom(startItemID=lastID)
        all_images = []
        test_counter = 0
        label = []
        lastID = resultJSON[-1]["id"]
        print(lastID)
        for item in resultJSON:
    #         print(item)
            response = requests.get(THUMBURL+item["thumb"])
            img = Image.open(BytesIO(response.content))
            img = resizeimage.resize_cover(img, [32, 32], validate=False)
            img.save(str(item["id"])+".jpeg", img.format)
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
            if test_counter>10:
                break
    
    np_imgarray = np.array(all_images,dtype=np.uint8)
    np_label = np.array(label,dtype=np.uint8)
    dump_dict = {"data":np_imgarray,"labels":np_label}
    pickle.dump( dump_dict, open( "save.p", "wb" ) )
        
#         input("next")
    
#     print(resultJSON)
if __name__ == "__main__":
    main()