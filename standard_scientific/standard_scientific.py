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

from dataclasses import dataclass
from decimal import Decimal
import re

__all__ = ['standard_scientific']
__version__ = '0.0.1'

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
#
#@dataclass 
#class Sigfig_SI:
#    '''Class for representing data in scientific notation with significant figures'''
#    value: float = None #the actual value as a python float
#    sigfigs: int = None #the number of significant figures
#    exponent: int = None #exponent (*10^Y, or EY, where Y is this exponent)
#
#    #from_float
#    @classmethod
#    def from_float(cls, value: float, sigfigs: int):
#        '''Given a python float and number of sigfigs, return a Sigfit_SI object''' 
#        assert(isinstance(float(values), float)), f"Value {value} could not be converted to float"
#        assert(isinstance(int(sigfigs), int)), f"Sigfigs {sigfigs} could not be converted to int"
#
#        self.value = float(value)
#        self.sigfigs = int(sigfigs) 
#        self.exponent = exponent_from_float(self.value) 
#
#    #from string
#
#    #to string
#
#    #add two Sigfig_SI
#
#    #multiply two Sigfig_SI
    

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
