import segment
import datetime

def parse(input):
    header = _convertToList(input.pop(0))
    if set(header) < set(['source', 'destination', 'departure', 'arrival', 'price', 'bags_allowed', 'bag_price', 'flight_number']):
        raise Exception('The given input does not satisfy the requirements.')
    for row in input:
        attrs = zip(header, _convertToList(row))
        result = _createSegment(attrs)
        yield result

def _createSegment(attrs):
    result = segment.Segment()
    for attr in attrs:
        value = attr[1]
        if set([attr[0]]) < set(['arrival', 'departure']):
            value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        elif set([attr[0]]) < set(['bags_allowed', 'bag_price', 'price']):
            value = int(value)
        setattr(result, attr[0], value)
    return result

def _convertToList(input):
    return input.replace("\n", "").split(',')
