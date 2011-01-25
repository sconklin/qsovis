#!/usr/bin/python
#
#import re
from Hamlib import *
from adif import *
from pysvg.structure import *
from pysvg.shape import *
import math

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
    x = distance * math.cos(angle)
    y = distance * math.sin(angle)
    return (x, y)

if __name__ == '__main__':

    scale = 500
    xoff = 20
    yoff = 20

    sz = svg("My test")

    recs = adifParse(sys.argv[1])
    for rec in recs:
        #print rec
        call = rec["call"]
        if not rec.has_key('gridsquare'):
            print "skipping " + call
            continue

        angle = angleFromTime(rec["time_on"])
        distance, azimuth = bearingDistance(rec["my_gridsquare"], rec["gridsquare"])
        distance = distance / scale
        print distance, azimuth
        bx, by = polar2Rect(distance, azimuth)
        blob = circle(bx + xoff, by + yoff, 0.25)
        sz.addElement(blob)
        #print call, angle, distance
        #print rec["freq_rx"]

    sz.save("./testout.svg")

