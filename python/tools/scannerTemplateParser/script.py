#! /usr/bin/env python3

import xml.etree.ElementTree as ET
from ibapi.scanner import ScannerSubscription 
from ibapi.tag_value import TagValue


#ScannerContent
# print(root[0].attrib)
#Intrument
# print(root[0][2].attrib)
#Scan type
# print(root[0][3].attrib)
#Advanced filter
# print(root[0][5])


def createScanner(xml):
    
    tree = ET.parse(xml)
    root = tree.getroot()

    scanContent = root[0].attrib
    instr = root[0][2].attrib
    scnType = root[0][3].attrib
    advFilter = root[0][5]

    scanner = ScannerSubscription()
    scanner.scanCode = scnType['scanCode']
    scanner.instrument = instr['m_type']
    scanner.locationCode = scanContent['locationText']
    if len(advFilter) != 0:
        tagValues = [TagValue(el.tag, el.text) for el in advFilter]

    return scanner, tagValues 

if __name__ == "__main__":

    s, t = createScanner('sampleScan.xml')
    print(s)
    print(t)
