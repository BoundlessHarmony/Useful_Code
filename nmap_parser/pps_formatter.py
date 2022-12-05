# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 20:09:26 2022

@author: Boundless
"""

import string

editThis=[]
writeThis=[]
nums = ''

with open("C:\\Users\\Boundless\\Documents\\Python Scripts\\nmap_parser\\pps_sample.txt") as f:
    lines = f.readlines()
    for line in lines:
        if line=='\n':
            next
        else:
            editThis.append(line)
    for line in editThis:
        for letter in line:
            if letter.isdigit():
                nums = nums + letter
        writeThis.append(nums + '\n')
        nums = ""
f.close()


with open("C:\\Users\\Boundless\\Documents\\Python Scripts\\nmap_parser\\pps_formatted.txt", 'w') as x:
    for line in writeThis[1:]:
        x.write(line)
    x.close()
print('hello')