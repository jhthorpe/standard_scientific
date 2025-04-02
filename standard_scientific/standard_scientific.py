# standard_scientific.py 
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

#################################################################################
# exponent_from_float
#
def exponent_from_float(x: float) -> int:
    '''Given a floating point number, determine the exponent used in its SI representation'''
    assert(isinstance(Decimal(x), Decimal)), f"Value {x} could not be converted to decimal" 

    (sign, digits, exponent) = Decimal(x).as_tuple()

    return len(digits) + exponent - 1


#################################################################################
# Sigfig
#
# A class that represents a piece of data in scientific notation and tracks its
# significant figures
#
# NOTE:
#   This uses the default dataclass constructors, which do NOT guarentee that
#   your significant figure data makes ANY sense at all. For example...
#
#   pi = Sigfig(value = 3.14, sigfigs = 2, exponent = -1)
#
# will have the following problems:
#   a. the value is 3.14 instead of 3.1, as indicated by the sigfigs
#   b. the value is 3.14 instead of 0.314, as indicated by the exponent
#
# To ensure correct construction, ALWAYS use the "from_float" function: 
#   pi = Sigfig.from_float(value = 3.14, sigfigs = 2)
#
#   pi.value = 3.1
#   pi.sigfigs = 2
#   pi.exponent = 0
#
#
@functools.total_ordering
@dataclass
class Sigfig:
    '''Class for representing data in scientific notation with significant figures'''
    value: float
    sigfigs: int
    exponent: int

    #########################################################
    # from_float
    # Generates a Sigfig from a floating point with the designated number of significant digits
    #
    @classmethod
    def from_float(cls, value: float, sigfigs: int):
        '''Given a python float and number of sigfigs, return a Sigfit_SI object''' 
        assert(isinstance(float(value), float)), f"Value {value} could not be converted to float."
        assert(isinstance(int(sigfigs), int)), f"Sigfigs {sigfigs} could not be converted to int."

        #now, we need to round the float to the sigfigs
        fv = float(value)
        sf = int(sigfigs)
        exp = exponent_from_float(fv)

        return Sigfig(value = round(fv, (sf - 1) - exp), sigfigs = sf, exponent = exp) 


    #########################################################
    # to string
    # returns a string of a given float to the designated number of significant figures  
    #

    ##################################################################
    # == (equality) 
    # 
    # NOTE:
    #   This has an override depending on if the other thing 
    #   is another Sigfig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise). That is, 
    #   the two values MUST agree 0.5 of one more digit than they are
    #   significant to.
    #
    def __eq__(self, other):
        if (isinstance(other, Sigfig)):
            return (self.sigfigs == other.sigfigs and
                    self.exponent == other.exponent and
                    abs(self.value - other.value) < (5.0 * pow(10., -self.sigfigs + self.exponent)))
        else:
            return self.value < other

    ##################################################################
    # < (strictly less than)
    #
    # NOTE:
    #   This one has an override dependong on if the other 
    #   this in another Sigfig object or just a "normal" number,
    #   though precision does not matter in this case
    #
    def __lt__(self, other):
        if (isinstance(other, Sigfig)):
            return self.value < other.value
        else:
            return self.value < other

    ##################################################################
    # + (add)
    #
    # NOTE: 
    #   This has an override depending on if the other thing 
    #   is another Sigfig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise)

    ##################################################################
    # - (subtract) 
    #
    # NOTE: 
    #   This has an override depending on if the other thing
    #   is another Sigfig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise)

    ##################################################################
    # * (multiply) 
    #
    # NOTE: 
    #   This has an override depending on if the other thing  
    #   is another Sigfig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise)

    ##################################################################
    # / (divide) 
    #
    # NOTE: 
    #   This has an override depending on if the other thing  
    #   is another Sigfig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise)

    

'''
@dataclass
class Standard_Scientific:
#    Class for representing values and uncertainties in scientific notatio
    value: float
    standard_uncertainty: float
    relative_standard_uncertainty: float
    value_sigfigs: int
    standard_uncertainty_sigfigs: int
    relative_standard_uncertainty_sigfigs: int
    units: str
    is_exact: bool = False

    #from string

    #to string

    #from_dict (for .json interface)
    #
    @classmethod
    def from_dict(cls, dictionary):
        return cls(value                = dictionary['value'],
                   standard_uncertainty = dictionary['standard_uncertainty'],
                   relative_standard_uncertainty = dictionary['relative_standard_uncertainty'])

    #to dict (for .json interface)

    #add

    #multiply

    #add_with_covariance

    #multiply_with_covariance
'''
