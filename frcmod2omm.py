'''
Script contains conversion factors and functions for FRCMOD to OMM 
conversion. Following parameters can be converted with this script.
    1. HarmonicBondForce
    2. HarmonicAngleForce
    3. PeriodicTorsionForce: Proper
    4. PeriodicTorsionForce: Improper
    5. NonbondedForce

@author: Madhuranga Rathnayake
'''


import math

radian2degree = 57.2957795130  # 1 rad  = 57.2957795130 degree
kcal2kj       = 4.184          # 1 kcal = 4.184 kj
ang2nm        = 0.1


def _bond(line):
    """(list:str) -> str
    Parameters: list: processed line from .frcmod file
    Return    : Force Constant (K) and min.dist (r)
        K: kcal/mol/(A**2)  ->  K/2: 2*kj/mol/nm**2
        r: Ang              ->  nm
    ----
    c3-h1  330.60   1.097
    """
    atoms = line[:5].replace('-', ' ').split()
    params = line[5:].split()
    k     = float(params[0])
    r     = float(params[1])

    omm_t1 = atoms[0]
    omm_t2 = atoms[1]
    omm_k  = 2*k*kcal2kj/(ang2nm*ang2nm)
    omm_r  = r*ang2nm

    omm_out = '<Bond type1="{}" type2="{}" length="{}" k="{}"/>'.format(omm_t1, omm_t2, omm_r, omm_k)
    
    print(omm_out)
    return(omm_out)


def _angle(line):
    """(list:str) -> str
    Parameters: list: processed line from .frcmod file
    Return    : Force Constant (K) and min.angle (a)
        K: kcal/mol/(rad**2)  ->  K/2: 2*kj/mol/(rad**2)
        a: degrees            ->  rad
    ----
    c3-n -c3   63.030     115.640
    """
    atoms  = line[:8].replace('-', ' ').split()
    params = line[8:].split()
    k      = float(params[0])
    a      = float(params[1])

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
    Parameters: list: processed line from .frcmod file
    Return    : Force Constant (K) and min.angle (a)
        K(PK/IDIVF): kcal  ->  K: kj/mol
        phase: degrees     ->  rad
    ----
    h1-c3-n -c3   6    0.000         0.000           2.000
    """
    atoms  = line[:11].replace('-', ' ').split()
    params = line[11:].split()
    idivf  = float(params[0])
    pk     = float(params[1])
    phase  = float(params[2])
    pn     = float(params[3])

    omm_t1 = atoms[0]
    omm_t2 = atoms[1]
    omm_t3 = atoms[2]
    omm_t4 = atoms[3]
    omm_k  = (pk/idivf) * kcal2kj
    omm_phase = math.radians(phase)
    omm_pn = int(pn)

    omm_out = '<Proper type1="{}" type2="{}" type3="{}" type4="{}" periodicity1="{}" phase1="{}" k1="{}"/>'.format(omm_t1, omm_t2, omm_t3, omm_t4, omm_pn, omm_phase, omm_k)

    print(omm_out)
    return(omm_out)



def _improper(line):
    """(list:str) -> str
    Parameters: list: processed line from .frcmod file
    Return    : Force Constant (K) and min.angle (a)
        K: kcal          ->  K: kj/mol
        phase: degrees   ->  rad
    ----
    c -c3-n -c3         1.1          180.0         2.0 
          ^
      out of plane
    """
    atoms  = line[:11].replace('-', ' ').split()
    params = line[11:].split()
    k      = float(params[0])
    phase  = float(params[1])
    pn     = float(params[2])

    omm_t1 = atoms[2]  # this is the one in out-of-plane. must go 1st in OMM
    omm_t2 = atoms[0]
    omm_t3 = atoms[1]
    omm_t4 = atoms[3]

    omm_k = k*kcal2kj
    omm_p = math.radians(phase)
    omm_pn = int(pn)

    omm_out = '<Improper type1="{}" type2="{}" type3="{}" type4="{}" periodicity1="{}" phase1="{}" k1="{}"/>'.format(omm_t1, omm_t2, omm_t3, omm_t4, omm_pn, omm_p, omm_k)

    print(omm_out)
    return(omm_out)


def _nonbonding(line):
    """(list:str) -> str
    Parameters: list: processed line from .frcmod file
    Return    : Force Constant (K) and min.angle (a)
        rmin/2: Ang       ->  nm
        epsilon: kcal/mol ->  kj/mol
    ----
    c3          1.9080  0.1094
    """  
    llist = line.split()
    sqrt62 = math.pow(2, 1/6)

    atom_t1  = llist[0]
    rmin2    = float(llist[1])
    epsilon  = float(llist[2]) 

    omm_sigma   = ang2nm * 2 * rmin2 / sqrt62
    omm_epsilon = kcal2kj * epsilon

    omm_out = '<Atom type="{}" charge="XXXX" sigma="{}" epsilon="{}"/>'.format(atom_t1, omm_sigma, omm_epsilon)

    print(omm_out)
    return(omm_out)

