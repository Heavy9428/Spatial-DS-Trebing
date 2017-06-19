import pprint as pp
import os
import sys


def read_crime_data_location(Map_Location):
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    keys = []
    crimes = []
    Crime_Locations =[]
    got_keys = False
    #with open(DIRPATH+'/../NYPD_CrimeData/Nypd_Crime_01') as f:
    with open(DIRPATH + '/NYPD_CrimeData'+ Map_Location) as f:
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not got_keys:
                keys = line
                got_keys = True
                continue
            crimes.append(line)
            # for crime in crimes:
            #     X = crime[21]
            #     Y = crime[22]
            #     Crime_Locations.append((X,Y))
    return crimes