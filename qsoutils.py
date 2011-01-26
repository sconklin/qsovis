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

#def isCanadianCall(call):
# CY0	Sable Is
# CY9	St-Paul Is
# VA1, VE1	New Brunswick, Nova Scotia
# VA2, VE2	Quebec
# VA3, VE3	Ontario
# VA4, VE4	Manitoba
# VA5, VE5	Saskatchewan
# VA6, VE6	Alberta
# VA7, VE7	British Columbia
# VE8	North West Territories
# VE9	New Brunswick
# VO1	Newfoundland
# VO2	Labrador
# VY0	Nunavut
# VY1	Yukon
# VY2	Prince Edward Island


def isUSCall(call):
# 1x2, 1x3, 2x1, 2x2, 2x3
#  /\b(([A-Z]{1,2})|([A-Z][0-9]))[0-9][A-Z]{1,3}\b/

# Prefixes (all followed by alpha only)
#
# [AKNW]L[0-7] Alaska
# [AKNW]H[67] Hawaii
#
# A[0-9]
# K[0-9]
# N[0-9]
# W[0-9]
#
# A[A-K][0-9]
# K[A-K, M-Z][0-9]
# N[A-K, M-Z][0-9]
# W[A-K, M-O, Q-Z][0-9]
#
    usregex = '^([AKNW]|A[A-K]|K[A-KM-Z]|N[A-KM-Z]|W[A-KM-OQ-Z])[0-9][A-Z]+'

    result = re.search(usregex, call, re.I)
    return result

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
