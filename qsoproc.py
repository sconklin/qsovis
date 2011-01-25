#!/usr/bin/python
#
#import re
from math import sin, cos, radians


from Hamlib import *
from adif import *

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *


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

if __name__ == '__main__':

    scale = 50
    dotsize = 5
    xoff = 300
    yoff = 300
    timelength = 180
    timetextlen = 190

    sz = svg("My test")
    sz.set_onload("init(evt)")

    # add the scripting
    sc = script()
    sc.set_xlink_href("mouse_over.js")
    sc.set_xlink_type("text/ecmascript")
    #xlink:href="mouse_over_effects.js" type="text/ecmascript"
    sz.addElement(sc)

    oh = ShapeBuilder()

    idcount = 0

    # draw 24 hour markers
    for hour in range (0, 24):
        ang = hour * 15
        tx, ty = polar2Rect(timelength, ang)
        sz.addElement(oh.createLine(xoff, yoff, xoff + tx, yoff + ty, strokewidth=2, stroke="black"))

        tx, ty = polar2Rect(timetextlen, ang-90)
        tt = str(hour)
        t = text(tt, tx + xoff, ty + yoff)
        sz.addElement(t)

    # Draw the text element for use with mouse events
    t = text("text box", xoff, 20)
    t.set_id("textNode")
    sz.addElement(t)

    # Draw the QSO points
    recs = adifParse(sys.argv[1])
    for rec in recs:
        #print rec
        call = rec["call"]
        if not rec.has_key('gridsquare'):
            print "skipping (no grid) " + call
            continue
        if not rec.has_key('freq'):
            print "skipping (freq) " + call
            continue

        angle = angleFromTime(rec["time_on"])
        distance, azimuth = bearingDistance(rec["my_gridsquare"], rec["gridsquare"])
        distance = distance / scale

        bx, by = polar2Rect(distance, angle-90)
        fillcolor = freq2Color(rec["freq"])

        eid = str(idcount)
        idcount = idcount + 1

        poptext = rec["call"] + " " + str(rec["freq"])

        dot = circle(bx + xoff, by + yoff, dotsize)
        dot.set_fill(fillcolor)
        dot.set_stroke('black')
        dot.set_id(eid)
        dot.set_onmouseover('showQSO("' + poptext + '")')
        dot.set_onmouseout('hideQSO()')
        dot.set_onclick('QSOClick("' + rec["call"] + '")')

        sz.addElement(dot)

    sz.save("./testout.svg")

