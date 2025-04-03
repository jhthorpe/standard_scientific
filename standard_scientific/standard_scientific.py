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
# SigFig
#
# A class that represents a piece of data in scientific notation and tracks its
# significant figures
#
# NOTE:
#   This uses the default dataclass constructors, which do NOT guarentee that
#   your significant figure data makes ANY sense at all. For example...
#
#   pi = SigFig(value = 3.14, sigfigs = 2, exponent = -1)
#
# will have the following problems:
#   a. the value is 3.14 instead of 3.1, as indicated by the sigfigs
#   b. the value is 3.14 instead of 0.314, as indicated by the exponent
#
# To ensure correct construction, ALWAYS use the "from_float" function: 
#   pi = SigFig.from_float(value = 3.14, sigfigs = 2)
#
#   pi.value = 3.1
#   pi.sigfigs = 2
#   pi.exponent = 0
#
#
@functools.total_ordering
@dataclass
class SigFig:
    '''Class for representing data in scientific notation with significant figures'''
    value: float
    sigfigs: int
    exponent: int

    #########################################################
    # from_float
    # Generates a SigFig from a floating point with the designated number of significant digits
    #
    @classmethod
    def from_float(cls, value: float, sigfigs: int):
        '''Given a python float and number of sigfigs, return a Sigfit_SI object''' 

        fv = float(value)
        sf = int(sigfigs)

        assert(isinstance(fv, float)), f"Value {value} could not be converted to float."
        assert(isinstance(sf, int)), f"SigFigs {sigfigs} could not be converted to int."
        assert(sf > 0), f"Requested sigfigs {sigfigs} cannot be less than 1"

        #now, we need to round the float to the sigfigs
        exp = exponent_from_float(fv)

        return SigFig(value = round(fv, (sf - 1) - exp), sigfigs = sf, exponent = exp) 


    #########################################################
    # to string
    # returns a string of a given float to the designated number of significant figures  
    #
    def __str__(self):
        return f"{self.value:.{self.sigfigs-1}e}"

    ##################################################################
    # == (equality) 
    # 
    # NOTE:
    #   This operation can ONLY be valid between two significant figures,
    #   since, by definition, we MUST know to how many significant digits we
    #   are comparing
    #
    def __eq__(self, other):
        if (isinstance(other, SigFig)):
            return (self.sigfigs == other.sigfigs and
                    self.exponent == other.exponent and
                    abs(self.value - other.value) < (5.0 * pow(10., -self.sigfigs + self.exponent)))
        else:
            return NotImplemented 

    ##################################################################
    # < (strictly less than)
    #
    # NOTE:
    #   This one has an override dependong on if the other 
    #   this in another SigFig object or just a "normal" number,
    #   though precision does not matter in this case since we
    #   ``always'' store the sigfig number via from_float
    #
    def __lt__(self, other):
        if (isinstance(other, SigFig)):
            return self.value < other.value
        else:
            return self.value < other

    ##################################################################
    # + (add)
    #
    # NOTE: 
    #   This has an override depending on if the other thing 
    #   is another SigFig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise and the sigfigs
    #   are just those of the original)
    #
    #   The rule is as follows. The number of digits of precision
    #   of the rounded result of adding two numbers must be 
    #   equivilant to the limitting number of digits of precision
    #   of the two numbers, and the number of significant figures 
    #   in the resulting value must be adjusted to make this true.
    #
    #   The limiting digits place is such that
    #       -1 is the tenths place,
    #        0 is the ones place
    #       +1 is the tens place
    #
    #   Then we always need to set the number of sig fig to 
    #   the power of the exponent of the result minus one less
    #   than this number
    #   
    #
    def __add__(self, other):
        if (isinstance(other, SigFig)):
            limd = max(-(self.sigfigs - 1) + self.exponent,
                       -(other.sigfigs - 1) + other.exponent)
            val = self.value + other.value
            ex = exponent_from_float(ex)
            return SigFig(value = val, sigfigs = ex - (limd - 1))
        else:
            limd = -(self.sigfigs - 1) + self.exponent
            val = self.value + other
            ex = exponent_from_float(ex)
            return SigFig(value = val, sigfigs = ex - (limd - 1))
    
    ##################################################################
    # - (subtract) 
    #
    # NOTE: 
    #   This has an override depending on if the other thing 
    #   is another SigFig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise and the sigfigs
    #   are just those of the original)
    #
    #   see __add__ for description
    #
    def __sub__(self, other):
        if (isinstance(other, SigFig)):
            limd = max(-(self.sigfigs - 1) + self.exponent,
                       -(other.sigfigs - 1) + other.exponent)
            val = self.value - other.value
            ex = exponent_from_float(ex)
            return SigFig(value = val, sigfigs = ex - (limd - 1))
        else:
            limd = -(self.sigfigs - 1) + self.exponent
            val = self.value - other
            ex = exponent_from_float(ex)
            return SigFig(value = val, sigfigs = ex - (limd - 1))
    

    ##################################################################
    # * (multiply) 
    #
    # NOTE: 
    #   This has an override depending on if the other thing 
    #   is another SigFig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise and the sigfigs
    #   are just those of the original)
    #
    #   The rule is as follows: we multiply the two numbers and take the
    #   result's significant figures as the minimum of the two input's 
    #   signifcant figures
    #
    def __mul__(self, other):
        if (isinstance(other, SigFig)):
            return SigFig.from_float(value = self.value * other.value, 
                                     sigfigs = min(self.sigfigs, other.sigfigs))
        else:
            return SigFig.from_float(value = self.value * other, 
                                     sigfigs = self.sigfigs)


    ##################################################################
    # / (divide) 
    #
    # NOTE: 
    #   This has an override depending on if the other thing 
    #   is another SigFig object or just a "normal" number (which 
    #   we will take to mean it is infinitely precise and the sigfigs
    #   are just those of the original)
    #
    #   The rule is as follows: we divide the two numbers and take the
    #   result's significant figures as the minimum of the two input's 
    #   signifcant figures
    #
    def __truediv__(self, other):
        if (isinstance(other, SigFig)):
            return SigFig.from_float(value = self.value / other.value, 
                                     sigfigs = min(self.sigfigs, other.sigfigs))
        else:
            return SigFig.from_float(value = self.value / float(other), 
                                     sigfigs = self.sigfigs)

    

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
