import sys
import myparser
import itinerary
import json

rawData = sys.stdin.readlines()

data = list(myparser.parse(rawData))

itineraries = []

def expandItineraries(validItineraries):
    nextItineraryWave = []
    for itinerary in validItineraries:
        nextItineraryWave.extend(itinerary.validNextItineraries(data))
    itineraries.extend(nextItineraryWave)
    if len(nextItineraryWave) > 0:
        expandItineraries(nextItineraryWave)

expandItineraries(map(lambda d: itinerary.Itinerary([d]), data))

def segmentsByBagsAllowed(bags_allowed):
    return list(itinerary for itinerary in itineraries if itinerary.bags_allowed>=bags_allowed)

def JSONByBagsAllowed(bags_allowed):
    return list(map(lambda s: s.asSerializable(bags_allowed), segmentsByBagsAllowed(bags_allowed)))

result = {'bag_count':{0: JSONByBagsAllowed(0), 1: JSONByBagsAllowed(1), 2: JSONByBagsAllowed(2)}}

if (len(sys.argv)>1) and (sys.argv[1]=='--compact'): #compact humanreadable list
    for i in range(3):
        print(str(i) + ' bags:')
        for nobag in segmentsByBagsAllowed(i):
            print('{0} to {1} for {2}, flights {3}'.format(
                nobag.source,
                nobag.destination,
                nobag.price(i),
                list(map(lambda a: a.flight_number,nobag.segments))))
else:
    print(json.dumps(result))
