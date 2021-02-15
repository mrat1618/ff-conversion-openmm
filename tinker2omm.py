#!/usr/bin/env python3

"""
Script contains conversion factors and functions for Tinker to OMM 
conversion. Following parameters can be converted with this script.
    1. multipole: handles only z-then-x local frame
    2. polarize : handles only 3 polarizable group connections 
    3. vdw
    4. bond
    5. angle : handles only a single angle
    6. strbnd
    7. torsion

Use main.py to perform the conversion. It'll print all converted lines 
in OMM format and unconverted lines in light grey. 

Doctests have been implemented and forced to print in verbose mode.

@author: Madhuranga Rathnayake
"""

from math import pi

radian = 57.2957795130 # 1 rad = 57.2957795130 degree   or could use math.radian()


def _atom(llist):
    pass


def _vdw(llist):
    """ (list) -> string

    Converts vdw parameters from Tinker to OpenMM format. 
        sigma      Å  ->  nm
        epsilon    kcal/mol	 ->  kJ/mol

    >>> llist = ['vdw', '26', '3.8000', '0.1010']  
    >>> _vdw(llist)  
    '<Vdw class="26" sigma="0.3800" epsilon="0.422584" reduction="1.0" />'

    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml 
    """
    atom_class = llist[1]
    sigma = float(llist[2]) * 0.1
    epsilon = float(llist[3]) * 4.184
    if len(llist) == 5:
        reduction = llist[4]
    else:
        reduction = 1.00
    omm_vdw = '<Vdw class="{}" sigma="{:.4f}" epsilon="{:.6f}" reduction="{}" />'.format(atom_class, sigma, epsilon, reduction)
    return(omm_vdw)


def _bond(llist):
    """ (list) -> string

    Converts bonding parameters from Tinker to OpenMM format.
        Force constant	  kcal/(mol*Å^2)  ->  kJ/(mol.nm^2)
        bond length	      Å  ->  nm

    >>> llist = ['bond', '6', '16', '341.00', '1.1120']
    >>> _bond(llist)
    '<Bond class1="6" class2="16" length="0.111200" k="142674.40" />'

    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml
    """
    atom_class1 = llist[1]
    atom_class2 = llist[2]
    k = float(llist[3]) * 4.184 / 0.01
    bond_length = float(llist[4]) * 0.1

    omm_bond = '<Bond class1="{}" class2="{}" length="{:.6f}" k="{:.2f}" />'.format(atom_class1, atom_class2, bond_length, k)

    return(omm_bond)


def _angle(llist):
    """ (list) -> string

    Converts bonding parameters from Tinker to OpenMM format.
        Force constant     kcal/(mol*rad^2)	 ->  kJ/(mol.degree^2)
        Angle	           degrees

    >>> llist = ['angle', '53', '54', '54', '69.20', '114.00']
    >>> _angle(llist)
    '<Angle class1="53" class2="54" class3="54" k="8.819673448e-02" angle1="114.00" />'
        
    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml
    # TODO: there can be multiple angles(implemented). --> add doc test
    """ 
    if len(llist) == 6:   
        atom_class1 = llist[1]
        atom_class2 = llist[2]
        atom_class3 = llist[3]
        k = float(llist[4]) * 4.184/(180/pi)**2
        angle = llist[5]

        omm_angle = '<Angle class1="{}" class2="{}" class3="{}" k="{:.9e}" angle1="{}" />'.format(atom_class1, atom_class2, atom_class3, k, angle)
    
    elif len(llist) == 8:
        atom_class1 = llist[1]
        atom_class2 = llist[2]
        atom_class3 = llist[3]
        k = float(llist[4]) * 4.184/(180/pi)**2
        angle1 = llist[5]
        angle2 = llist[6]

        omm_angle = '<Angle class1="{}" class2="{}" class3="{}" k="{:.9e}" angle1="{}" angle2="{}" />'.format(atom_class1, atom_class2, atom_class3, k, angle1, angle2)

    elif len(llist) == 9:
        atom_class1 = llist[1]
        atom_class2 = llist[2]
        atom_class3 = llist[3]
        k = float(llist[4]) * 4.184/(180/pi)**2
        angle1 = llist[5]
        angle2 = llist[6]
        angle3 = llist[7]

        omm_angle = '<Angle class1="{}" class2="{}" class3="{}" k="{:.9e}" angle1="{}" angle2="{}" angle3="{}" />'.format(atom_class1, atom_class2, atom_class3, k, angle1, angle2, angle3)
    
    else:
        print('something wrong with AMOEBA angles!')
        print(llist)

    return(omm_angle)


def _strbend(llist):
    """ (list) -> string

    Converts stertch-bend parameters from Tinker to OpenMM format.
        k	kcal/(ang.rad.mol)  ->  kJ/(nm.degree.mol)

    >>> llist = ['strbnd', '6', '7', '30', '11.50', '11.50']
    >>> _strbend(llist)
    '<StretchBend class1="6" class2="7" class3="30" k1="8.397826229e+00" k2="8.397826229e+00" />'

    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml
    """
    atom_class1 = llist[1]
    atom_class2 = llist[2]
    atom_class3 = llist[3]
    k1 = float(llist[4]) * (4.184*10 / (180/pi))
    k2 = float(llist[5]) * (4.184*10 / (180/pi))

    omm_StretchBend = '<StretchBend class1="{}" class2="{}" class3="{}" k1="{:.9e}" k2="{:.9e}" />'.format(atom_class1, atom_class2, atom_class3, k1, k2)

    return(omm_StretchBend)


def _torsion(llist):
    """ (list) -> string

    Converts torsion parameters from Tinker to OpenMM format.
        k	         kcal    ->  kJ/2
        phase	     degree  ->  rad
        periodicity	 integer ->  integer

    >>> llist = ['torsion', '39', '1', '8', '8', '0.982', '0.0', '1', '0.994', '180.0', '2', '0.170', '0.0', '3']
    >>> _torsion(llist)
    '<Proper class1="39" class2="1" class3="8" class4="8"   k1="2.054344" phase1="0.000000000000" periodicity1="1"   k2="2.079448" phase2="3.141592653590" periodicity2="2"   k3="0.355640" phase3="0.000000000000" periodicity3="3" />'
    
    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml
    """
    atom_class1 = llist[1]
    atom_class2 = llist[2]
    atom_class3 = llist[3]
    atom_class4 = llist[4]

    k1 = float(llist[5]) * (4.184/2)
    phase1 = float(llist[6]) * (pi/180)
    periodicity1 = llist[7]

    k2 = float(llist[8]) * (4.184/2)
    phase2 = float(llist[9]) * (pi/180)
    periodicity2 = llist[10]

    k3 = float(llist[11]) * (4.184/2)
    phase3 = float(llist[12]) * (pi/180)
    periodicity3 = llist[13]

    omm_torsion = '<Proper class1="{}" class2="{}" class3="{}" class4="{}"   k1="{:.6f}" phase1="{:.12f}" periodicity1="{}"   k2="{:.6f}" phase2="{:.12f}" periodicity2="{}"   k3="{:.6f}" phase3="{:.12f}" periodicity3="{}" />'.format(atom_class1, atom_class2, atom_class3, atom_class4, k1, phase1, periodicity1, k2, phase2, periodicity2, k3, phase3, periodicity3)

    return(omm_torsion)


def _polarize(llist):
    """ (list) -> string

    Converts polarizability parameters from Tinker to OpenMM format.
        polarize  Ang^3  ->  nm^3

    >>> llist = ['polarize','253','1.7500','0.3900','252','254','257']
    >>> _polarize(llist)
    '<Polarize type="253" polarizability="0.001750" thole="0.3900" pgrp1="252" pgrp2="254" pgrp3="257" />'


    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml
    # TODO: there can be upto 5 pol groups. extend 3 to 5 groups
    """
    atom_class1 = llist[1]
    polarizability = float(llist[2]) * 0.001
    thole_damping_factor = llist[3]
    try:
        polarizable_groups = llist[4:]
    except:
        polarizable_groups = []

    if not polarizable_groups:
        omm_polarize = '<Polarize type="{}" polarizability="{:.6f}" thole="{}" />'.format(atom_class1, polarizability, thole_damping_factor)

    elif len(polarizable_groups) == 1:
        omm_polarize = '<Polarize type="{}" polarizability="{:.6f}" thole="{}" pgrp1="{}" />'.format(atom_class1, polarizability, thole_damping_factor, polarizable_groups[0])
    
    elif len(llist) == 6:
        omm_polarize = '<Polarize type="{}" polarizability="{:.6f}" thole="{}" pgrp1="{}" pgrp2="{}" />'.format(atom_class1, polarizability, thole_damping_factor, polarizable_groups[0], polarizable_groups[1])

    elif len(llist) == 7:
        omm_polarize = '<Polarize type="{}" polarizability="{:.6f}" thole="{}" pgrp1="{}" pgrp2="{}" pgrp3="{}" />'.format(atom_class1, polarizability, thole_damping_factor, polarizable_groups[0], polarizable_groups[1], polarizable_groups[2])
    else:
        print("error in polarize parameters")
        print(llist)

    return(omm_polarize)


def _multipole(llist):
    """  (list) -> string

    Converts multipole parameters (monopole, dipole and quadrapole) from Tinker to OpenMM format.
        c0  monopole     e
        dx  dipole	     e.bohr  -->  e.nm 
        qxx quadrupole	 (e.bohr^2)/3  ->  (e.nm^2)/3

    >>> llist = ['multipole', '7', '44', '10', '-0.14168', '0.07684', '0.00000', '0.42468', '0.07677', '0.00000', '-1.10639', '-0.13195', '0.00000', '1.02962']
    >>> _multipole(llist)
    '<Multipole type="7" kz="44" kx="10" c0="-0.141680" d1="4.066197670806e-03" d2="0.000000000000e+00" d3="2.247309769440e-02" q11="7.165929777951e-05" q21="0.000000000000e+00" q22="-1.032735840436e-03" q31="-1.231658765404e-04" q32="0.000000000000e+00" q33="9.610765426565e-04" />'

    TODO: correct following test!
    >>> llist2 = ['multipole', '189', '190', '-191', '-191', '0.28761', '0.34263', '0.00000', '0.97464', '-0.69101', '0.00000', '0.85372', '-0.23783', '0.00000', '-0.16271']
    
    <Multipole type="236" kz="33" kx="-237" ky="-237" c0="-0.29203" d1="0.0207236378428" d2="0.0" d3="0.0157800643602" q11="-0.000767660845211" q21="0.0" q22="0.000281802032039" q31="-0.000249113369694" q32="0.0" q33="0.000485858813172"  />

    Doctesting inputs and outputs were taken from amoebabio09.prm and amoeba2009.xml
    # TODO: only z-then-x frame parameter conversion is available. implement parameter converion for other local frames
    """
    bohr = 0.52917720859

    if len(llist) == 14:
        atom = llist[1]
        kz = llist[2]
        kx = llist[3]

        c0 = float(llist[4])

        d1 = float(llist[5]) * bohr*0.1
        d2 = float(llist[6]) * bohr*0.1
        d3 = float(llist[7]) * bohr*0.1

        q11 = float(llist[8]) * 0.01*bohr*bohr/3.0
        q21 = float(llist[9]) * 0.01*bohr*bohr/3.0
        q22 = float(llist[10]) * 0.01*bohr*bohr/3.0
        q31 = float(llist[11]) * 0.01*bohr*bohr/3.0
        q32 = float(llist[12]) * 0.01*bohr*bohr/3.0
        q33 = float(llist[13]) * 0.01*bohr*bohr/3.0

        omm_multipole = '<Multipole type="{}" kz="{}" kx="{}" c0="{:.6f}" d1="{:.12e}" d2="{:.12e}" d3="{:.12e}" q11="{:.12e}" q21="{:.12e}" q22="{:.12e}" q31="{:.12e}" q32="{:.12e}" q33="{:.12e}" />'.format(atom, kz, kx, c0, d1, d2, d3, q11, q21, q22, q31, q32, q33)
    
    elif len(llist) == 15:
        atom = llist[1]
        kz = llist[2]
        kx = llist[3]
        ky = llist[4]

        c0 = float(llist[5])

        d1 = float(llist[6]) * bohr*0.1
        d2 = float(llist[7]) * bohr*0.1
        d3 = float(llist[8]) * bohr*0.1

        q11 = float(llist[9]) * 0.01*bohr*bohr/3.0
        q21 = float(llist[10]) * 0.01*bohr*bohr/3.0
        q22 = float(llist[11]) * 0.01*bohr*bohr/3.0
        q31 = float(llist[12]) * 0.01*bohr*bohr/3.0
        q32 = float(llist[13]) * 0.01*bohr*bohr/3.0
        q33 = float(llist[14]) * 0.01*bohr*bohr/3.0

        omm_multipole = '<Multipole type="{}" kz="{}" kx="{}" ky="{}" c0="{:.6f}" d1="{:.12e}" d2="{:.12e}" d3="{:.12e}" q11="{:.12e}" q21="{:.12e}" q22="{:.12e}" q31="{:.12e}" q32="{:.12e}" q33="{:.12e}" />'.format(atom, kz, kx, ky, c0, d1, d2, d3, q11, q21, q22, q31, q32, q33)

    return(omm_multipole)


def _opbend(llist):
    ''' (list) -> string
    convert out of plane tinker parameters to openmm

    >>> llist = ["opbend", "2", "1", "0", "0", "41.70"]
    >>> _opbend(llist)
    '<Angle class1="2" class2="1" class3="0" class4="0" k="5.314745416e-02"/>'
    '''

    atom_class1 = llist[1]
    atom_class2 = llist[2]
    atom_class3 = llist[3]
    atom_class4 = llist[4]

    radian2 = 4.184/(radian*radian)
    k = float(llist[5]) * radian2

    omm_opbend = '<Angle class1="{}" class2="{}" class3="{}" class4="{}" k="{:.9e}"/>'.format(atom_class1, atom_class2, atom_class3, atom_class4, k)

    return(omm_opbend)


def _pitors(llist):
    ''' (string list) -> string
    convert tinker pi torsions to openmm 

    >>> llist = ["pitors", "1", "3", "6.85"]
    >>> _pitors(llist)
    '<PiTorsion class1="1" class2="3" k="28.6604" />'
    '''
    
    piTorsionUnit = 1.0
    conversion = 4.184*piTorsionUnit

    atom_class1 = llist[1]
    atom_class2 = llist[2]

    k = float(llist[3])*conversion

    omm_pitors = '<PiTorsion class1="{}" class2="{}" k="{:.4f}" />'.format(atom_class1, atom_class2, k)

    return(omm_pitors)

# do automate testing when running this script.
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)