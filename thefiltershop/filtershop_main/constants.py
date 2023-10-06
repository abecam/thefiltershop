from enum import Enum

SPOTLIGHT_LIMIT = 100

class Studio_and_Publisher_Size(Enum):
    ARTISAN = (0, 5)
    INDIE = (6, 20)
    MEDIUM = (21, 50)
    BIG = (51, 1000)
    HUGE = (1001, 10000)
    
    
    def __init__(self, min, max):

        self.min = min
        self.max = max