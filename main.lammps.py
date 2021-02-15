#!/usr/bin/env python3

"""
Core routines for LAMMPS to OMM parameter conversion. This will print 
all converted lines in OMM format and unconverted lines in light grey.

NOTE: 
    - Intend to use in bash environment. Grey colour rendering only
      works in bash.
    - File handling kept default. Path problems might occur depending 
      on OS distribution. 

USAGE: script.py <lig.param>

@Author: Madhuranga Rathnayake
"""
import lammps2omm as lmm
import sys

# grey colour bash text variable. marks unconverted lines in less pronounced light grey colour.
CGREY = '\33[90m'
CEND = '\33[0m'

# check system arguments and extract input lammps parameter file
# exit if there's no input parameter file specified.
if len(sys.argv) == 2:
    fname = sys.argv[1]
else:
    print('No LAMMPS param file specified!')
    print('USAGE: script.py lig.param')
    sys.exit()


# start conversion
with open(fname, 'r') as params:
    for line in params:
        cleaned_line = line.strip()
        if len(cleaned_line) >= 1 and cleaned_line.split()[0] == "bond_coeff":
            omm_out = lmm._bond(cleaned_line)
        elif len(cleaned_line) >= 1 and cleaned_line.split()[0] == "angle_coeff":
            omm_out = lmm._angle(cleaned_line)
        elif len(cleaned_line) >= 1 and cleaned_line.split()[0] == "dihedral_coeff":
            omm_out = lmm._dihedral(cleaned_line)
        elif len(cleaned_line) >= 1 and cleaned_line.split()[0] == "pair_coeff":
            omm_out = lmm._nonbonding(cleaned_line)
        else:
            print(CGREY+cleaned_line+CEND)
