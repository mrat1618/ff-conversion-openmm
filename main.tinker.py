#!/usr/bin/env python3

"""
Main script for Tinker to OMM parameter conversion. This will print 
all converted lines in OMM format and unconverted lines in light grey.

USAGE: script.py tinker-parameter-file.prm

NOTE: 
    - Intend to use in bash environment. Grey colour rendering only
      works in bash.
    - File handling kept default. Path problems might occur depending 
      on OS distribution. 

USAGE: script.py <tinker-parameter-file.prm>z

@Author: Madhuranga Rathnayake
"""

import tinker2omm as t2omm
import sys

# check system arguments and extract input tinker parameter file
# exit if there's no input parameter file specified
if len(sys.argv) == 2:
    input_file = sys.argv[1]
else:
    print('No AMOEBA Force Field file specified!')
    print('USAGE: script.py tinker-parameter-file.prm')
    sys.exit()

# grey colour bash text variable. marks unconverted lines in less pronounced light grey colour.
CGREY = '\33[90m'
CEND = '\33[0m'

# open Tinker parameter file to read
file = open(input_file, 'r')

# read file line by line
for line in file:
    # strip parameters and remove line breaks
    line_in_list = line.strip().split()

    # skip comments and lines with less than 3 items
    # if True, skips the loop
    if len(line_in_list) < 3 or line_in_list[0].startswith('#'):
        pass

    # convert bonds
    elif line_in_list[0].startswith('bond'):
        omm_bond_param = t2omm._bond(line_in_list)
        print(omm_bond_param)

    # convert angles
    elif line_in_list[0].startswith('angle'):
        omm_angle_param = t2omm._angle(line_in_list)
        print(omm_angle_param)

    # convert Stretch-Bends
    elif line_in_list[0].startswith('strbnd'):
        omm_strbnd_param = t2omm._strbend(line_in_list)
        print(omm_strbnd_param)

    # convert torsions
    elif line_in_list[0].startswith('torsion'):
        omm_torsion_param = t2omm._torsion(line_in_list)
        print(omm_torsion_param)

    # convert vdw
    elif line_in_list[0].startswith('vdw'):
        omm_vdw_param = t2omm._vdw(line_in_list)
        print(omm_vdw_param)

    # convert out of plane bending
    elif line_in_list[0].startswith('opbend'):
        omm_opbend_param = t2omm._opbend(line_in_list)
        print(omm_opbend_param)

    # convert pitorsions
    elif line_in_list[0].startswith('pitors'):
        omm_pitors_param = t2omm._pitors(line_in_list)
        print(omm_pitors_param)

    # convert multipoles - monopole, dipole and quadrapoles
    elif line_in_list[0].startswith('multipole'):
        dipoles = file.readline().strip().split()
        multipoles1 = file.readline().strip().split()
        multipoles2 = file.readline().strip().split()
        multipoles3 = file.readline().strip().split()

        # creates a single list with all monopole + dipole + quadrapoles
        multipoles_list = line_in_list + dipoles + multipoles1 +multipoles2 + multipoles3

        omm_multipoles = t2omm._multipole(multipoles_list)
        print(omm_multipoles)

    # convert polarizability
    elif line_in_list[0].startswith('polarize'):
        omm_polarize_param = t2omm._polarize(line_in_list)
        print(omm_polarize_param)

    elif line_in_list[0].startswith('opbend'):
        omm_opbend_param = t2omm._opbend(line_in_list)
        print(omm_opbend_param)
    
    # print skipped lines in light grey colour
    else:
        print(CGREY + 'skipping line:  ' + line.strip() + CEND)

# done reading, close the parameter file
file.close()