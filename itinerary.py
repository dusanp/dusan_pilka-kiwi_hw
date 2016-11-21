import datetime
import json

class Itinerary:

    def __init__(self, segments):
        self.segments = segments

    segments = []

    def price(self, bag_count):
        return sum(map(lambda s: s.price+(s.bag_price*bag_count),self.segments))

    @property
    def bags_allowed(self):
        return min(map(lambda s: s.bags_allowed, self.segments))

    @property
    def source(self):
        return self.segments[0].source

    @property
    def destination(self):
        return self.segments[-1].destination

    def validNextItineraries(self, data):
        for validNextSegment in (segment for segment in data if self._isValidNextSegment(segment)):
            result = Itinerary(self.segments + [validNextSegment])
            yield result

    def _isValidNextSegment(self, segment):
        #mulitple ifs for readability
        if set([(segment.source, segment.destination)]) < set(map(lambda s: (s.source, s.destination), self.segments)):
            return False #same segment is already in this route

        lastSegment = self.segments[-1]
        transferTime = segment.departure - lastSegment.arrival
        if (transferTime > datetime.timedelta(hours=4)) or (transferTime < datetime.timedelta(hours=1)): #1-4 hours inclusive
            return False

        return segment.source == lastSegment.destination

    def asSerializable(self, bag_count=0):
        return {
            'source': self.source,
            'destination': self.destination,
            'price': self.price(bag_count),
            'bags_allowed': self.bags_allowed,
            'bag_count': bag_count,
            'itinerary': list(map(lambda s: s.asSerializable(), self.segments)),
        }
