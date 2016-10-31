#! /usr/bin python
# -*- coding: utf-8 -*-

"""
Name: objectlist_splus_01.py
Version 0.1
Description: Provide a list of observed OBJECT to be transfered
Author: Walter Santos
Created on: Nov 28th 2016
Last Updated: Nov 31th 2016
Latest Changes:
Instructions: Run the code with a -h/--help option to list all the arguments,
necessary and optional, on the command line.
Requirements:
"""

"""
IMPORTS
"""

import argparse
import os
import os.path
from astropy.io import fits
import time


"""
FUNCTIONS
"""



"""
MAIN
"""
parser = argparse.ArgumentParser(description='S-PLUS OBJECT list generator')
parser.add_argument('-n','--night', default=None, help='night data \
                    to be considered. Default is "today"', metavar='yyyy/mm/dd or yyyymmdd')
parser.add_argument('-o','--output', default=None, help='output file name, better \
                    use default objectlist_yyyymmdd', metavar='output_file')
parser.add_argument('-p','--path', default='', help='path to the images')

"""
python objectlist_splus_01.py -n "2016/10/30"

TIP: If you are running the script inside the same folder as the images are,
then set the night to ''.
"""

"""
Parse the input parameters, define and declare variables
"""
args = parser.parse_args()
settings = vars(args)

today = time.localtime()
night = '%i%i%i' % (today.tm_year, today.tm_mon, today.tm_mday)

if settings['night'] is not None:
    night = settings['night'].replace('/','')

path = settings['path']+night

filenames = list()
for f in os.walk(path)[2]:
    if os.path.splitext(f)[1].lower() is '.fits':
        filenames.append(f)

objectlist = list()
for f in filenames:
    try:
        hdr = fits.open(f)[0].header
    except:
        print('WARNING: Unable to open or corrupted file '+f+'. Ignoring it.\n')
    else:
        try:
            obj = hdr['OBJECT']
        except:
            print('WARNING: Unable to find keyword OBJECT in file '+f+'. Ignoring it.\n')
        else:
            objectlist.append(obj)

output = 'objectList_'+night
if settings['output'] is not None:
    output = settings['output']

out = open(output, 'a+')
objectlistOrig = out.readlines()

objectlist = list(set(objectlist+objectlistOrig))

out.close()