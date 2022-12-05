# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Perform a compare on a given Normally formatted nmap file against a list of approved PPS


import xml.etree.ElementTree as ET

#to learn xml.etree.ElementTree refer to 
# https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# read element objects section before doing things

#init scan list -
scan = []
pps =[]

fPath = "C:\\Users\\Boundless\\Documents\\Python Scripts\\nmap_parser\\sampleAllportsLoopback.xml"
app_pps = "C:\\Users\\Boundless\\Documents\\Python Scripts\\nmap_parser\\pps_formatted.txt"

# print(type(test))
tree = ET.parse(fPath)
root = tree.getroot()

#check elements
# elements = []
# for elem in tree.iter():
#     elements.append(elem.tag)
# print(elements)

#found em dear


# print(root.attrib)

# for child in root.iter('ports'):
#     print(child.tag, child.attrib)


for p in root.iter('port'):
    pNums = p.get('portid')
    pState = p.get('state')
    pServ = p.get('service')
    scan.append(pNums)
print(type(scan[1]))

scan = [int(p) for p in scan]

with open(app_pps, 'r') as f:
    lines = f.readlines()
    for line in lines:
        pps.append(line)

pps = [int(p) for p in pps]
print(pps)


# if scanl not in app_pps, then check it out
for port in scan:
    if port not in pps:
        print(port, " " , "<~~~~~~~~~~ Correct This")

#YUGE SUCCESS! WE FOUND AN ELEMENT WITH DESIRED SUB ELEMENTS