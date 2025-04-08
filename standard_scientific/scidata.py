# scidata.py 
#
# Python package for representing values in scientific notation, including
# significant figures.
#
# c = Standard_Scientific.from_string("299 792 458 m s", is_exact=True)
#
# c.value == 2.99792458e8
# c.units == "m s"
# c.value_sigfigs == 9
# c.standard_uncertainty == None
#
# me = Standard_Scientific.from_string("9.109 383 7139(28) × 10−31 kg")
#
# me.value == 9.1093837139e-31
# me.standard_uncertainty == 0.0000000023e-31 
# me.relative_standard_uncertainty = 3.1e-10
# me.standard_uncertainty_sigfigs == 2
#
# Revision History:
#   April 2, 2025 : JHT created
#

import functools
from dataclasses import dataclass
from decimal import Decimal
import re
import numpy as np
import warnings
from standard_scientific.sigfig import SigFig 

eps = np.finfo(float).eps

class foobar:
    def __init__(self):
        self.x = 5
        self.y = 6.

#################################################################################
# SciData 
#
# Class designed to help manage data in scientific notation, including 
# sig figs and uncertainties
#
@functools.total_ordering
@dataclass
class SciData:
    '''Class for representing values and uncertaintines in scientific notation'''
    value: SigFig
    unc: SigFig
    rel_unc: SigFig
    is_exact: bool

    #Note, default initialization will come from dataclass decorator 

    ##########################
    # from string
    # 
    # Generates values in scientific notatoin from a string
    #
    # Here is the most general case(s):
    #   12.345(67) x 10-23
    #   12.345(67) E-23
    #   "12.345[[(67)] [x10[-]23]]"
    #
    # Or, equivilantly
    #
    # 
    # Which should be interpreted as the following fields:  
    # 
    #

    ##########################
    # from_floats 
    #
    # Generate the class from SigFig classes. There are 
    # four cases:
    # 
    # 1) The value is exact and there is no uncertainty
    #       -> Create exact SciData 
    # 2a) The data is inexact but rel_unc and unc are both given 
    #       -> Store data. NOTE, we do NOT check that rel_unc ==
    #          value / unc (with sigfigs) 
    # 2b) The data is inexact and rel_unc is not given
    #       -> Generate the relative uncertainty from the sig figs 
    # 2c) We are not given the uncertainty at all and we are not exact
    #       -> This must error!
    #
    # NOTE: given the floating point numerical issues of uncertainties near cutoffs between 
    #       SigFig classes, we do not STRICTLY require that the relative uncertainty be rigerously
    #       identical to the uncertainty divided by the value. 
    #
    @classmethod
    def from_SigFigs(cls, value: SigFig, unc: SigFig, rel_unc: SigFig, is_exact=False):

        #in case of non-exact data 
        if not is_exact:

            assert(isinstance(value, SigFig)), "{value} was not an instance of scientific_notation:SigFig ."
            assert(isinstance(unc,   SigFig)), "{unc} was not an instance of scientific_notation:SigFig ."
            assert(isinstance(rel_unc, SigFig) or rel_unc is None), "{rel_unc} was not an instance of scientific_notation:SigFig or None."

            # We have a relative uncertainty
            if not rel_unc is None:
                return SciData(value = value, unc = unc, rel_unc = rel_unc, is_exact = False) 

            # We do NOT have a relative uncertainty, use SigFig division
            else:
                return SciData(value = value, unc = unc, rel_unc = unc / value, is_exact = False) 

        #in case of exact data
        else:
            assert(isinstance(value, SigFig)), "{value} was not an instance of scientific_notation:SigFig ."
            return SciData(value = value, unc = None, rel_unc = None, is_exact = True) 




    ##########################
    # .json inferfaces
    #To dict

    #from Dict

    
    ##########################
    # Add, substract
    #
    # Note that there are TWO versions of this function, 
    #
    # Note that the uncertainty propogation 
    # in this case defaults to the "no covariance" case, 
    # which is not correct but is what I imagine most 
    # users would want.
    
    
    ##########################
    # Mult. Div. 
    # 
    # default: with covariance value 
    #
    # no_covar: no covariance value 
    

    ##########################
    # __eq__ comparison
    #
    # This is the strict comparison of objects, 
    # not the statistical version that should be used
    # in scientific litt. Note that these comparisions will 
    # be SigFig comparisions!
    #
    def __eq__(self, other):
        if (not self.is_exact and not other.is_exact):
            return (self.value == other.value and
                 self.unc == other.unc and
                 self.rel_unc == other.rel_unc and
                 self.is_exact == other.is_exact)
        elif (self.is_exact and other.is_exact):
            return (self.value == other.value)
        return False
     

    ##########################
    # __lt__ comparison
    #
    # This tests strict lt comparison of the values, not the
    # statistical probability that should be used in scientific
    # litt.
    #
    def __lt__(self, other):
        return (self.value < other.value)
