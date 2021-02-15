'''
Script contains conversion factors and functions for LAMMPS to OMM 
conversion. Following parameters can be converted with this script.
    1. pair_coeff (LJ)
    2. bond_coeff
    3. angle_coeff
    4. dihedral_coeff

NOTE: This script is specifically made to help to param convertion process 
of MYP type potentials parameters to OpenMM. 

@author: Madhuranga Rathnayake
'''

import math

radian2degree = 57.2957795130  # 1 rad  = 57.2957795130 degree
kcal2kj       = 4.184          # 1 kcal = 4.184 kj
ang2nm        = 0.1

# grey colour bash text variable. marks unconverted lines in less pronounced light grey colour.
CGREY = '\33[90m'
CYLW = '\33[33m'
CEND = '\33[0m'


def _bond(line):
    """(list:str) -> str
    Parameters: list: processed line from lammps param file
    Return    : Force Constant (K) and min.dist (r)
        K: kcal/mol/(A**2)  ->  K/2: 2*kj/mol/nm**2 (scale factor 2)
        r: Ang                ->  nm
    ----
    bond_coeff  1  338.69999999999999        1.0910000000000000  # c3-hx
    0           1  2                         3                   4 5    
                ^  ^                         ^
                   K                         r
    """
    llist     = line.split()
    # bond_type = llist[1]
    atoms = llist[5].split('-')
    k         = float(llist[2])
    r         = float(llist[3])

    omm_k  = k * 2*kcal2kj/(ang2nm*ang2nm)
    omm_r  = r * ang2nm

    omm_out = '<Bond type1="{}" type2="{}" length="{}" k="{}"/>'.format(atoms[0], atoms[1], omm_r, omm_k)
    
    print(omm_out)
    return(omm_out)


def _angle(line):
    """(list:str) -> str
    Parameters: list: processed line from lammps param file
    Return    : Force Constant (K) and min.angle (a)
        K: kcal/mol/(rad**2)  ->  K/2: 2*kj/mol/(rad**2) (scale factor 2)
        a: degrees            ->  rad
    ----
    angle_coeff  1  46.200000000000010        110.10999693591019  # c3-n4-hn 
    0            1  2                         3                   4 5
                    ^                         ^              
                    K                         a    
    """
    llist  = line.split()
    atoms  = llist[5].split('-')
    k      = float(llist[2])
    a      = float(llist[3])

    omm_t1 = atoms[0]
    omm_t2 = atoms[1]
    omm_t3 = atoms[2]
    omm_k  = 2*k*kcal2kj
    omm_a  = math.radians(a)

    omm_out = '<Angle type1="{}" type2="{}" type3="{}" angle="{}" k="{}"/>'.format(omm_t1, omm_t2, omm_t3, omm_a, omm_k)

    print(omm_out)
    return(omm_out)


def _dihedral(line):
    """(list:str) -> str
    CHARMM dihedral
    Parameters: list: processed line from lammps param file
    Return    : 
        K:kcal/mol                      ->  K: kj/mol
        periodicity(n): integer >= 0    ->  int
        d(phase offset): degrees        ->  rad
        weigh.fac: read more at https://lammps.sandia.gov/doc/dihedral_charmm.html
                   must kept 0 for AMBER type lj/cut

    ----
    dihedral_coeff  1  0.15559999999999999     3   0   0.00000000    # hx-c3-n4-hn
    0               1  2                       3   4   5             6 7
                       ^                       ^   ^   ^           
                       K                       n   d   weigh.fac
    """
    llist  = line.split()
    atoms  = llist[7].split('-')

    k           = float(llist[2])
    periodicity = int(llist[3]) 
    phaseoffset = int(llist[4])

    omm_t1 = atoms[0]
    omm_t2 = atoms[1]
    omm_t3 = atoms[2]
    omm_t4 = atoms[3]
    omm_k  = k * kcal2kj
    omm_periodicity = periodicity
    omm_phaseoffset = math.radians(phaseoffset)    

    omm_out = '<Proper type1="{}" type2="{}" type3="{}" type4="{}" periodicity1="{}" phase1="{}" k1="{}"/>'.format(omm_t1, omm_t2, omm_t3, omm_t4, omm_periodicity, omm_phaseoffset, omm_k)

    print(omm_out)
    return(omm_out)


def _nonbonding(line):
    """(list:str) -> str
    Parameters: list: processed line from lammps param file
    Return    : Force Constant (K) and min.angle (a)
        epsilon: kcal/mol       ->  kj/mol
        sigma  : angstrom       ->  nm       
    ----
    pair_coeff   1 3   lj/charmm/coul/long   1.4000000000000000E-002   2.2645400000000002  # pb-hn
    0            1 2   3                     4                         5                   6 7
                                             ^                         ^
                                             epsilon                   sigma
    """  
    llist = line.split()

    atom_type1 = llist[1]
    atom_type2 = llist[2]
    epsilon    = float(llist[4]) 
    sigma      = float(llist[5]) 

    omm_sigma   = ang2nm * sigma
    omm_epsilon = kcal2kj * epsilon

    # only output LJ pairs with same atom type
    if atom_type1 == atom_type2 and llist[3].startswith("lj"):
        atom_type2_name = llist[7].split('-')[1]
        omm_out = '<Atom type="{}" charge="XXXX" sigma="{}" epsilon="{}"/>'.format(atom_type2_name, omm_sigma, omm_epsilon)
        print(omm_out)
    elif atom_type1 != atom_type2 and llist[3].startswith("lj"):
        print(CGREY + line.strip() + CEND)
        print(CYLW+"    {}   omm_sigma={}   omm_epsilon={}".format(llist[7], omm_sigma, omm_epsilon)+CEND)
        omm_out=""
    else:
        print(CGREY + line.strip() + CEND)
        omm_out=""

    if atom_type1 == atom_type2 and llist[3].startswith("buck"):
        atom_type2_name = llist[8].split('-')[1]
        omm_buck = '<Atom type="{}" charge="XXXX" sigma="0.0" epsilon="0.0"/>'.format(atom_type2_name)
        print(omm_buck)    
    
    return(omm_out)

