import datetime
from collections import namedtuple

Departure = namedtuple('Departure','scheduled actual')

def get_departures():
    departures = []
    with open('amtrak-data.txt') as f:
        for line in f.readlines():
            departure = get_departure(line)
            if departure:
                departures.append(departure)
    return departures

def get_departure(line):
    '''Return a tuple containing two datetime.datetime objects.'''
    if line[0] == '*':
        return None

    departure = line.strip().split('\t')

    if len(departure) <= 1:
        return None

    planned_departure = datetime.datetime.strptime(departure[0][:-5],
                                      '%m/%d/%Y %I:%M %p')
    actual_departure = datetime.datetime.strptime(departure[0][:10] +
                                     departure[1],
                                     '%m/%d/%Y%I:%M%p')

    #return (planned_departure, actual_departure)
    return Departure(planned_departure, actual_departure)

def main():
    departures = get_departures()
    #ontime_departures = [d for d in departures if d[1] == d[0]]
    ontime_departures = [d for d in departures if d.scheduled == d.actual]
    #late_departures = [d for d in departures if d[1] > d[0]]
    late_departures = [d for d in departures if d.actual > d.scheduled]
    other_departures = [d for d in departures if d.actual < d.scheduled]
    next_day_departures = [d for d in departures if
                           d[0].day != d[1].day]

    print('''Total Departures: {}
Ontime Departures: {}
Late Departures: {}
Other Departures: {}
Next Day Departures: {}'''.format(len(departures),
                                   len(ontime_departures),
                                   len(late_departures),
                                  other_departures,
                                   len(next_day_departures)))

main()
