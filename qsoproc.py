#!/usr/bin/python
#
# TODO:
# Add parameter and option parsing
# Fix 'clock' display to use TZ and display midnight at top
# Add filter buttons
# Get the colors right
# Make hover text appear over the spot
#
import re
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

from qsoutils import *

if __name__ == '__main__':

    tz = -6
    scale = 30
    dotsize = 3
    xoff = 500
    yoff = 500
    timelength = 180
    timetextlen = 190

    # create the svg document itself
    sz = svg("My test")

    # add the scripting
    sc = script()
    sc.set_xlink_href("mouse_over.js")
    sc.set_xlink_type("text/ecmascript")
    sz.addElement(sc)
    sz.set_onload("init(evt)")

    oh = ShapeBuilder()

    idcount = 0

    # draw 24 hour markers
    for hour in range (0, 24):
        ang = hour * 15
        tx, ty = polar2Rect(timelength, ang)
        sz.addElement(oh.createLine(xoff, yoff, xoff + tx, yoff + ty, strokewidth=2, stroke="black"))

        tx, ty = polar2Rect(timetextlen, ang-90)
        dh = hour - 6
        if dh < 0:
            dh = dh + 24
        tt = str(dh)
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
            #print "skipping (no grid) " + call
            continue
        if not rec.has_key('freq'):
            #print "skipping (freq) " + call
            continue

        if isUSCall(call):
            print "skipping (US) " + call
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

