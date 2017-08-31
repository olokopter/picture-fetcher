
import requests
class Api:
    
    API_URL = "http://pr0gramm.com/api/"
    def __init__(self):
        self.flags = 0

    def enableNSFW(self):
        self.flags += 2
                
    def disableNSFW(self):
        self.flags -= 2
        
    def enableSFW(self):
        self.flags += 1
        
    def disableSFW(self):
        self.flags -= 1

    def getAllFrom(self, startItemID=None):
        # Set up the arguments for the REST call.
        args = ({
            'flags': self.flags,
            'promoted': 1,
            
        })
        if  startItemID:
            args[0]["older"]=startItemID
        
        
        # Make the request and verify success.
        url = self.API_URL + 'items/get'
        response = requests.get(url, params= args)
        response.raise_for_status()
        return response.json()["items"]

    def info(self, itemid):
        args = ({
             'itemId': itemid
        })
        
        url = self.server + 'items/info'
        response = requests.get(url, params= args)
        response.raise_for_status()
        return response.json()