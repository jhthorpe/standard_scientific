# scidata.py 
#
# Contains the SciData class and associated functions which help in the
# creation and manipulation of scientific data. The key difference here
# are the explicit use of significant figures and supporting measures
# of uncertainty. 
#
# Revision History:
#   April 2, 2025 : JHT created
#
#

#imports from within this package
from standard_scientific.float_compare import eps
from standard_scientific.sigfig import SigFig 
from standard_scientific.sigfig import exponent_from_float

#external imports
import functools
from dataclasses import dataclass
import numpy as np
import re

#################################################################################
# SciData 
#
# Class designed to help manage data in scientific notation, including 
# sig figs and uncertainties.
#
# NOTE: It is HIGHLY RECOMMENDED that you use the "from_SigFigs" or "from_str"
#       constructors rather than the constructors generated by the @dataclass
#       decorator, as these will NOT perform the correctness checking routines
#       supported by the other functions.
#
#       Additionally, the "from_SigFigs" constructor does NOT check that the
#       relative uncertainty (when given) is equal to the uncertainty divided by 
#       the value, as the relative uncertainty may be sensitive to numerical
#       errors in the rounding in SigFig.  
#
@functools.total_ordering
@dataclass
class SciData:
    '''Class for representing values and uncertaintines in scientific notation'''
    value: SigFig
    unc: SigFig
    rel_unc: SigFig
    is_exact: bool

    # Note, default initialization will come from dataclass decorator and will NOT
    # perform any correctness checking.

    ##########################
    # from_str
    # 
    # Generates values in scientific notatoin from a string
    #
    # Here is the most general case(s):
    #   12.345(67) x 10-23
    #   "12.345[[(67)] [x10[-]23]]"
    #  
    # This classmethod is specifically intended to be useful in parsing 
    # text data from online sources (such as CODATA, IUPAC, etc.)
    #
    # NOTE: 
    #   There are many many more ways that you can format this string
    #   badly than there are to do it correctly. Rather than protect 
    #   against ALL of them, we will simply trust that the number of ways to 
    #   format this correctly *that python will accept as a valid conversion 
    #   to floating point numbers* is relatively slim
    #
    @classmethod
    def from_str(cls, s):

        # Defaults should all cause errors on SigFig construction unless we specifically
        # override them later
        val = None
        unc = None
        rel = None
        exact = None
        val_sfig = None
        unc_sfig = None
        rel_sfig = None

        #characters that indicate the start of the exponent section 
        #after removal of whitespace
        #
        # NOTE: annoyingly, it MATTERS that x10** and x10^ is searched before
        #       x10, because x10 is a substring of both and we need avoid making * 
        #       and ^ characters in the exponent split of the string
        exponent_strings = ["e", "E", "x10**", "x10^", "x10"]
        start_strings = ["+", "-"] #valid start strings

        #start by trimming whitespace
        s_in = s
        s = "".join(s.split()) 

        #Now, if we have an exponent section, extract it. 
        #NOTE, this intentionally keeps badly formated strings with multiple
        #      matches which will fail upon float conversion (and need to be caught) 
        s_pow = "0" #default exponent power 
        f_exp = None #default exponent
        for sub in exponent_strings:
            if sub in s:
                s, s_pow = s.split(sub)
                break
        try:
            f_exp = pow(10., int(s_pow))
        except Exception as e:
            assert(False), f"Exception was thrown while attempting to extract exponent of {s_in}. {e}"


        # Check for uncertainty string 
        # 
        # Case a) the standard uncertainty string exists, extract
        #        
        # Case b) there is no uncertainty string and this is an "exact" value
        s_unc = None
        if ("(" in s and ")" in s):
            exact = False

            #extract the uncertainty string from the value string
            s, s_unc = s.split("(")
            s_unc, s_tmp = s_unc.split(")")
        else:
            exact = True

        try: 
            val = float(s) * f_exp
        except Exception as e:
            assert(False), f"Exception was thrown while attempting to extract exact value in {s_in}. {e}"

        # Obtain sigfigs of the value.
        #
        # When first writing this package, I used the following convention, but later decided that this was
        # likely to cause more problems than it resolved thanks to users expecting "exact" values (which may 
        # NOT have been created in an exact way...) to be identical to floating point values. As such, I've instead
        # opted to implement the "as_exact()" feature, and (aggrivatingly), set the number of sigfigs 
        # to the number of significant digits entered in the string. 
        #
        # OLD CASES:
        #
        # OLD Case a) The value is not exact, and the number of sigfigs are
        #         the number of digits in the significant digits string 
        #
        # OLD Case b) The value is exact and contains a decimal. The sigfigs
        #         are either the number of digits that are safe within machine
        #         precision or the number of digits actually present in the string,
        #         whichever is smaller.
        #
        # OLD Case c) The value is exact and does not contain a decimal. The sigfigs
        #         are the number of digits safe within machie precision.
        #

        s_sfig = re.sub('^[+-0]*0+', '', s) #remove all leading zero's following zero or signs 
        s_sfig = re.sub("^[.]0+", '', s_sfig) #remove any of the leading zero's that follow a decimal point in first position
        
        # NEW defintion of sig figs in a value
        val_sfig = sum(c.isdigit() for c in s_sfig)

        # OLD distinction between various "kinds" of exact values
        # if not exact:
        #    val_sfig = sum(c.isdigit() for c in s_sfig)
        # else:
        #    if "." in s:
        #        val_sfig = sum(c.isdigit() for c in s_sfig)
        #        val_sfig = min(val_sfig, exponent_from_float(val) - exponent_from_float(val * eps))
        #    else:
        #        val_sfig = exponent_from_float(val) - exponent_from_float(val * eps)

        # Value is done, save it's sigfig
        value_SigFig = SigFig.from_float(value = val, sigfigs = val_sfig)

        # If inexact, process the uncertainties 
        #
        # For this, we specifically need to 
        # a) determine the number of sigfigs in the uncertainty. Note that, here, we are less forgiving,
        #    and rigerously demand that the string cannot contain anything but digits, and that 
        #    the first value must be a nonzero number (no leading zero strings). We implicitly assume 
        #    that all trailing zeros are significant
        #
        # b) Find the exponent to multiply by. This takes place in three steps, detailed below:
        #    1. Convert to scientific notation exonent: 12.345(67) E-4 -> 1.2345(67) E-3, performed above 
        #    2. Find the decimal place the sigfig lives in: unc_sfig - val_sfig: 1.2345(67) -> 2 - 5 = -3  
        #    3. Convert the sigfig from integer to leading decimal form: -(unc_sfig - 1) 
        # 
        #    This all results in an exponent of :
        #       10^(value_exponent + value_sigfig + 1)
        #
        if not exact:

            unc_sfig = sum(c.isdigit() for c in s_unc)
            assert(unc_sfig == len(s_unc)), f"Uncertainty string in {s_in} contained non-digit characters."
            assert(s_unc[0] != "0"), f"Uncertainty string in {s_in} contained a leading 0" 

            try:
                #convert to int
                i_unc = int(s_unc)
                unc = i_unc  * pow(10., -val_sfig + 1 + value_SigFig.exponent) #WRONG
                assert(unc > 0), f"Standard uncertainty of <= 0 found in {s_in}." 
            except Exception as e:
                assert(False), f"Exception was thrown during the extraction of the uncertainty in {s_in}. {e}"

        #Generate the sigfigs
        unc_SigFig = SigFig.from_float(value = unc, sigfigs = unc_sfig) if not exact else None 
        rel_SigFig = unc_SigFig / abs(value_SigFig) if not exact else None

        return SciData(value = value_SigFig, unc = unc_SigFig, rel_unc = rel_SigFig, is_exact = exact) 

    ##########################
    # from_SigFigs 
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

            assert(isinstance(value, SigFig)), f"{value} was not an instance of scientific_notation:SigFig ."
            assert(isinstance(unc,   SigFig)), f"{unc} was not an instance of scientific_notation:SigFig ."
            assert(isinstance(rel_unc, SigFig) or 
                   rel_unc is None), f"{rel_unc} was not an instance of scientific_notation:SigFig or None."

            # We have a relative uncertainty
            if not rel_unc is None:
                return SciData(value = value, unc = unc, rel_unc = rel_unc, is_exact = False) 

            # We do NOT have a relative uncertainty, use SigFig division
            else:
                return SciData(value = value, unc = unc, rel_unc = unc / abs(value), is_exact = False) 

        #in case of exact data
        else:
            assert(isinstance(value, SigFig)), f"{value} was not an instance of scientific_notation:SigFig ."
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
    # NOTE that the comparisons here break down if the value gets too close to 0.000000......e0
    #
    def __eq__(self, other):
        if (isinstance(other, SciData)):
            if (not self.is_exact and not other.is_exact):
                return (self.value == other.value and
                     self.unc == other.unc and
                     self.rel_unc == other.rel_unc and
                     self.is_exact == other.is_exact)
            else:
                return abs(self.as_exact() - other.as_exact()) < max(abs(self.as_exact()), abs(other.as_exact())) * eps 
        else:
            assert(False), f"__eq__ is only defined between two instances of the SciData class" 
     

    ##########################
    # __lt__ comparison
    #
    # This tests strict lt comparison of the values, not the
    # statistical probability that should be used in scientific
    # litt.
    #
    def __lt__(self, other):
        if (isinstance(other, SciData)):
            return (self.value < other.value)
        else:
            return (self.value < other)

    ##########################
    # as_exact()
    # 
    # returns the value this data as if it was exact (infinite sigfigs)
    def as_exact(self):
        return self.value.as_exact()

    ##########################
    # string conversion
    def __str__(self):
        if self.is_exact:
            return f"{self.value.value * pow(10, -self.value.exponent):.{self.value.sigfigs}} (exact) E{self.value.exponent}" 
        else:
            return f"{self.value.value * pow(10, -self.value.exponent):.{self.value.sigfigs}} ({int(self.unc.value * pow(10, -self.unc.exponent + self.unc.sigfigs - 1 )):d}) E{self.value.exponent}" 
