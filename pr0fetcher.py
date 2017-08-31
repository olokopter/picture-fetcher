import pr0Api
from PIL import Image
import requests
from io import BytesIO
from resizeimage import resizeimage
THUMBURL = "http://thumb.pr0gramm.com/"
def main():
    api = pr0Api.Api()
    api.enableNSFW()
    resultJSON = api.getAllFrom()
    for item in resultJSON:
        print(item)
        response = requests.get(THUMBURL+item["thumb"])
        img = Image.open(BytesIO(response.content))
        img.save(str(item["id"])+".jpeg", img.format)
        input("next")
    
    print(resultJSON)
if __name__ == "__main__":
    main()