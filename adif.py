# !/usr/bin/python
import re
import sys
import xml.parsers.expat

# http://www.kb8lfa.com/2010/09/21/adif-parser-adding-adix-support/

def adifFixup(rec):
    if rec.has_key('band') and not rec.has_key('band_rx'):
        rec['band_rx'] = rec['band']
    if rec.has_key('freq') and not rec.has_key('freq_rx'):
        rec['freq_rx'] = rec['freq']
    if not rec.has_key('freq') and not rec.has_key('freq_rx'):
        rec['freq_rx'] = 0.0
        rec['freq'] = 0.0

def adiParse(raw):
    # Find the EOH, in this simple example we are skipping
    # header parsing.
    pos = 0
    m = re.search('<eoh>', raw, re.IGNORECASE)
    if m != None:
        # Start parsing our ADIF file after the <EOH> marker
        pos = m.end()

    recs = []
    rec = dict()
    while 1:
        # Find our next field definition <...>
        pos = raw.find('<', pos)
        if pos == -1:
            return recs
        endPos = raw.find('>', pos)

        # Split to get individual field elements out
        fieldDef = raw[pos + 1:endPos].split(':')
        fieldName = fieldDef[0].lower()
        if fieldName == 'eor':
            adifFixup(rec)     # fill in information from lookups
            recs.append(rec)   # append this record to our records list
            rec = dict()       # start a new record

            pos = endPos
        elif len(fieldDef) > 1:
            # We have a field definition with a length, get it's
            # length and then assign the value to the dictionary
            fieldLen = int(fieldDef[1])
            rec[fieldName] = raw[endPos + 1:endPos + fieldLen + 1].replace('&lt;', '<')
        pos = endPos
    return recs

def startElement(name, attrs):
    global fieldName

    fieldName = name.lower()

def endElement(name):
    global recs, rec

    if name == "record":
        adifFixup(rec)
        recs.append(rec)
        rec = dict()

def charData(data):
    global rec, fieldName

    data = data.rstrip()
    if len(data) > 0 and fieldName != None:
        rec[fieldName] = data

def adixParse(raw):
    global fieldName, rec, recs

    fieldName = None
    rec = dict()
    recs = []

    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = startElement
    p.EndElementHandler = endElement
    p.CharacterDataHandler = charData
    p.Parse(raw)
    return recs

def adifParse(filename):
    fh = open(filename, 'r')
    content = fh.read()
    fh.close()

    isXml = content.find("<?xml")
    if isXml > -1:
        return adixParse(content)
    else:
        return adiParse(content)

if __name__ == '__main__':
    recs = adifParse(sys.argv[1])
    print "start"
    for rec in recs:
        print rec
