from Event import DeviceEvent
class DataNormalizer:
    def __init__(self):
        pass
        #import some library functions to setup chain of responsibility design pattern
    def transform_first(self, data):
        #do some processing 
        return data
    def normalize(self, data):
        data = self.transform_first(data)
        return data
