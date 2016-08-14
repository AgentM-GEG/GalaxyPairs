'''
See Hogg 2000, sec.4, equations (14) and (15) for the calculation of the
comoving distances
'''
import numpy as np

# Cosmological Constants
c = 299792458
H0 = 70 * (1 / (3.08567758 * 10**19))
om_m = 0.3
om_k = 0.0
om_A = 0.7

def f(z, om_m, om_k, om_A):
    '''
    Defines the function to be integrated.

    Arguments:
    z - redshift (variable)
    om_m - omega matter
    om_k - omega curvature
    om_A - omega lambda

    The return value is a tuple, with the first element holding the estimated
    value of the integral and the second element holding an upper bound on the
    error.
    '''
    return (om_m * ((1 + z)**3) + om_k * ((1 + z)**2) + om_A)**(-0.5)

def integrate(startx, endx, steps):
    '''
    Performs the integration of the function
    '''
    width = (float(endx) - float(startx))/steps
    runningsum = 0
    for i in range(steps):
        height = f(startx + i*width, om_m, om_k, om_A)
        area = height*width
        runningsum +=area
    return runningsum

class galaxy(object):

    def __init__(self, TFIT_ID=0, RA=0.0, Dec=0.0, redshift=0.0, logM=0.0,Hmag=0.0):
        self.TFIT_ID = TFIT_ID
        self.RA = RA * np.pi / 180
        self.Dec = Dec * np.pi / 180
        self.z = redshift
        self.mass = float (10.0 ** logM)
        self.Hmag = float(Hmag)

    def __str__(self):
        return str(self.TFIT_ID)

    def __repr__(self):
        return self.__str__()

    def radialComovingDistance(self):
        '''
        Line-of-sight distance (kpc)
        NOTE: I have confirmed that this outputs the correct value when compared
        to Ned Wright's Cosmology Calculator.
        '''
        return ((c / H0) * integrate(0, self.z, 10000) *(1.0/(1+self.z))* (1 / (3.08567758 * 10**19))) #the end of this line is to convert from meters to kpc