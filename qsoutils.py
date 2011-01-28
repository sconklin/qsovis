#!/usr/bin/python
#
import re
from math import sin, cos, radians

from Hamlib import *

#
# based on a 24 hour clock
#
# 360 degrees = 24 hours
# degrees = 15 * (hours + minutes/60 + seconds/3600)
#

def angleFromTime(time):
    hr = float(time[0:2])
    mn = float(time[2:4])
    sc = float(time[4:6])
    return 15 * (hr + (mn/60) + (sc/3600))

def bearingDistance(myLoc, oLoc):
    status, mylon, mylat = locator2longlat(myLoc)
    status, olon, olat = locator2longlat(oLoc)
    status, distance, azimuth = qrb(mylon, mylat, olon, olat)
    # km, degrees - earth's circumference is about 40,000 km
    # so max distance is about 20,000 km
    return (distance, azimuth)

def polar2Rect(distance, angle):
    x = distance * cos(radians(angle))
    y = distance * sin(radians(angle))
    return (x, y)

def freq2Color(freqstr):
    freq = float(freqstr)
    if (freq >= 1.8) and (freq <= 2.0):
        # 160m
        return 'lawngreen';
    elif (freq >= 3.5) and (freq <= 4.0):
        # 80m
        return 'darkviolet';
    elif (freq >= 5.3) and (freq <= 5.5):
        # 60m
        return 'midnightblue';
    elif (freq >= 7.0) and (freq <= 7.3):
        # 40m
        return 'cornflowerblue';
    elif (freq >= 10.1) and (freq <= 10.150):
        # 30m
        return 'seagreen';
    elif (freq >= 14.0) and (freq <= 14.350):
        # 20m
        return 'goldenrod';
    elif (freq >= 18.068) and (freq <= 18.168):
        # 17m
        return 'khaki';
    elif (freq >= 21.0) and (freq <= 21.450):
        # 15m
        return 'tan';
    elif (freq >= 24.890) and (freq <= 24.990):
        # 12m
        return 'brown';
    elif (freq >= 28.0) and (freq <= 29.7):
        # 10m
        return 'mediumorchid';
    elif (freq >= 50.0) and (freq <= 54.0):
        # 6m
        return 'red';
    else:
        # Unknown 
        return 'dimgrey';

class qsoFilter:
    # __init__
    #
    def __init__(self, debug = False):
        self.debug = debug
        self.filters = {
            'Continental US': {'enabled':0, 'regex':'^([AKNW]|A[A-K]|K[A-KM-Z]|N[A-KM-Z]|W[A-KM-OQ-Z])[0-9][A-Z]+'},
            'Alaska': {'enabled':0, 'regex':'^[AKNW]L[0-7]+'},
            'Hawaii': {'enabled':0, 'regex':'^[AKNW]H[67]+'},
            'Canada': {'enabled':0, 'regex':'^(VA[1-7]|VE[1-9|VY[0-2]|VO[12]|CY[09])+'},
            'Mexico': {'enabled':0, 'regex':'^(XE[1-3]|XF[1-4])+'}
            }

    def loadFromFile(self, filename):
        # load the filters from a json file
        return

    def saveToFile(self, filename):
        # save the filters to a json file
        return

    def enable(self, fname):
        # turn on the filter
        fil = self.filters[fname]
        fil['enabled'] = 1
        return

    def disable(self, fname):
        # turn off the filter
        fil = self.filters[fname]
        fil['enabled'] = 0
        return

    def filterCall(self, call):
        # return TRUE if call passes filters
        for filname, fil in self.filters.items():
            if self.debug:
                print "Trying filter ", filname
            if fil['enabled']:
                if re.search(fil['regex'], call, re.I):
                    if self.debug:
                        print "Callsign " + call + " matches filter for " + filname
                    return False
        
        return True
