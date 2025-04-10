# float_compare.py
#
# Subpackage within standard_scientific that standardizes
# the comparision of floats in this package
#
#   Major Revision History:
#       April 10, 2025 @ ANL : created
#

import numpy as np

eps = float(np.finfo(float).eps)

#####################
# This routine is used for the float comparison, BUT
# have problems when x and y get sufficiently close to zero
# where |0| * eps = 0, and results in false negative where
# two numbers near zero look like they differ when they don't
def equal_floats(x, y): 
    return abs(x - y) < max(abs(x), abs(y)) * eps
