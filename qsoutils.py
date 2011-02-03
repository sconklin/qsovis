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

#class Menu:
#    # __init__
#    #
#    def __init__(self, debug = False):
#        self.debug = debug
#        self.style = None
#
#    def Button(self, x, y, ):




class Frequency:
    # __init__
    #
    def __init__(self, debug = False):
        self.debug = debug
        self.unknown_color = 'dimgrey'
        self.bands = {
            '160m': {'filtered': 0, 'min': 1.8, 'max': 2.0, 'color': 'lawngreen'},
            '80m': {'filtered': 0, 'min': 3.5, 'max': 4.0, 'color': 'darkviolet'},
            '60m': {'filtered': 0, 'min': 5.3, 'max': 5.5, 'color': 'midnightblue'},
            '40m': {'filtered': 0, 'min': 7.0, 'max': 7.3, 'color': 'cornflowerblue'},
            '30m': {'filtered': 0, 'min': 10.1, 'max': 10.150, 'color': 'seagreen'},
            '20m': {'filtered': 0, 'min': 14.0, 'max': 14.350, 'color': 'goldenrod'},
            '17m': {'filtered': 0, 'min': 18.068, 'max': 18.168, 'color': 'khaki'},
            '15m': {'filtered': 0, 'min': 21.0, 'max': 21.450, 'color': 'tan'},
            '12m': {'filtered': 0, 'min': 24.890, 'max': 24.990, 'color': 'brown'},
            '10m': {'filtered': 0, 'min': 28.0, 'max': 29.7, 'color': 'mediumorchid'},
            '6m': {'filtered': 0, 'min': 50.0, 'max': 54.0, 'color': 'red'}
            }

    def getColor(self, freq, filterme = True):
        # return None if it's filtered, unless overridden
        for bandname, band in self.bands.items():
            if (float(freq) >= band['min']) and (float(freq) <= band['max']):
                if band['filtered'] and filterme:
                    return None
                else:
                    return (band['color'])
                
        return self.unknown_color
                                
class CallFilter:
    # __init__
    #
    def __init__(self, debug = False):
        self.debug = debug
        self.filters = {
            'Continental US': {'filtered':0, 'regex':'^([AKNW]|A[A-K]|K[A-KM-Z]|N[A-KM-Z]|W[A-KM-OQ-Z])[0-9][A-Z]+'},
            'Alaska': {'filtered':0, 'regex':'^[AKNW]L[0-7]+'},
            'Hawaii': {'filtered':0, 'regex':'^[AKNW]H[67]+'},
            'Canada': {'filtered':0, 'regex':'^(VA[1-7]|VE[1-9|VY[0-2]|VO[12]|CY[09])+'},
            'Mexico': {'filtered':0, 'regex':'^(XE[1-3]|XF[1-4])+'}
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
        fil['filtered'] = 1
        return

    def disable(self, fname):
        # turn off the filter
        fil = self.filters[fname]
        fil['filtered'] = 0
        return

    def filterCall(self, call):
        # return TRUE if call passes filters
        for filname, fil in self.filters.items():
            if self.debug:
                print "Trying filter ", filname
            if fil['filtered']:
                if re.search(fil['regex'], call, re.I):
                    if self.debug:
                        print "Callsign " + call + " matches filter for " + filname
                    return False
        
        return True
