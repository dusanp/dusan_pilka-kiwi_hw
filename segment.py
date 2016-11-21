import myparser
import datetime

class Segment:
    def asSerializable(self):
        return dict(zip(self.__dict__, map(lambda v: str(v) if type(v) is datetime.datetime else v, self.__dict__.values())))
