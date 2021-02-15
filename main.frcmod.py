#!/usr/bin/env python3

"""
Main script for FRCMOD to OMM parameter conversion. This will print 
all converted lines in OMM format and unconverted lines in light grey.

NOTE: 
    - Intend to use in bash environment.
    - File handling kept default. Path problems might occur depending 
      on OS distribution. 

USAGE: script.py <lig.frcmod>

@Author: Madhuranga Rathnayake
"""

import frcmod2omm as fmm
import sys

# check system arguments and extract input frcmod parameter file
# exit if there's no input parameter file specified
if len(sys.argv) == 2:
    fname = sys.argv[1]
else:
    print('No FRCMOD file specified!')
    print('USAGE: script.py lig.frcmod')
    sys.exit()


def extract(fname, component):
    """(str: full line) -> list
    extract components from frcmod file
    """
    llist       = []
    empty_lines = 0

    ffrcmod = open(fname, 'r')

    for line in ffrcmod:
        if line.startswith(component):
            while not empty_lines:
                temp_line = ffrcmod.readline().strip()
                if len(temp_line) > 0:
                    llist.append(temp_line)
                else:
                    empty_lines += 1
                    break
        elif empty_lines > 0:
            break    

    ffrcmod.close()

    return(llist)


# extract
BOND     = extract(fname, "BOND")
ANGLE    = extract(fname, "ANGLE")
DIHE     = extract(fname, "DIHE")
IMPROPER = extract(fname, "IMPROPER")
NONBON   = extract(fname, "NONBON")

#print
for item in BOND:
    ommb = fmm._bond(item)
print("")

for item in ANGLE:
    ommb = fmm._angle(item)
print("")

for item in DIHE:
    ommb = fmm._dihedral(item)
print("")

for item in IMPROPER:
    ommb = fmm._improper(item)
print("")

for item in NONBON:
    ommb = fmm._nonbonding(item)
print("")
