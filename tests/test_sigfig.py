# test_sigfig.py
#
# Provides interface with Pytest for testing the sigfigs class
# and related functionality

import pytest

import standard_scientific as si 

###############################################################
# check that from_exponent gives correct exponentials
#
@pytest.mark.parametrize("x, r", [
    (3.14, 0),
    (10, 1),
    (1e6, 6),
    (578, 2),
    (1e-3, -3),
    (-10e-3, -2),
    (0.0015, -3)
    ])
def test_exponent_from_float(x, r):
    assert(si.exponent_from_float(x) ==  r)
    
###############################################################
# check that from_exponent gives error on nonsense input
#
@pytest.mark.parametrize("x", [
    (None),
    ('abc')
])
def test_exponent_from_float_excpetions(x):
    with pytest.raises(Exception) as e:
        si.exponent_from_float(x)


###############################################################
# check that from_float gives error on nonsense input
#
@pytest.mark.parametrize("x, y", [
    (None, None),
    (None, 1),
    (1, None),
    (1.234, 0),
])
def test_bad_construction(x, y):
    with pytest.raises(Exception) as e:
        si.SigFig.from_float(value = x, sigfigs = y)

###############################################################
# Check that .from_float with reasonable input gives the right 
#   values 
#
@pytest.mark.parametrize("x, s, v, e", [
    (3.14, 2, 3.1, 0),
    (1.23456e10, 6, 1.23456e10, 10),
    (-12.34e-2, 5, -1.2340e-1, -1)
    ])
def test_from_float(x, s, v, e):
    a = si.SigFig.from_float(x, s)
    assert(a.value == v)
    assert(a.exponent == e)
    assert(a.sigfigs == s)


###############################################################
# check that the .sigfig_place() function returns the 
# correct definition of the places
@pytest.mark.parametrize("x, y, p", [
    (210.123, 6, -3),
    (210.12 , 5, -2),
    (210.1  , 4, -1),
    (210    , 3,  0),
    (2.1e2  , 2,  1),
    (2e2    , 1,  2)
    ])
def test_sigfig_place(x, y, p):
    a = si.SigFig.from_float(x, y)
    assert(a.sigfig_place() == p)

###############################################################
# check the == operator for SigFig == SigFig
#
@pytest.mark.parametrize("x, s, y, t", [
    (3.14, 2, 3.13, 2)
    ])
def test_equals_SF_SF(x, s, y, t):
    assert(si.SigFig.from_float(x, s) == si.SigFig.from_float(y,t))

###############################################################
# check the != operator for SigFig != SigFig
#
@pytest.mark.parametrize("x, s, y, t", [
    (3.14, 2, 3.16, 2)
    ])
def test_not_equals_SF_SF(x, s, y, t):
    assert(si.SigFig.from_float(x, s) != si.SigFig.from_float(y,t))

###############################################################
# check the == operator for SigFig == float 
#
@pytest.mark.parametrize("x, s, f", [
    (10034.44, 7, 10034.44),
    (10034.44, 7, 10034.4449),
    (10034.44, 7, 10034.4365)
    ])
def test_equals_SF_f(x, s, f):
    assert(si.SigFig.from_float(x, s) == f)

###############################################################
# check the != operator for SigFig != float 
#
@pytest.mark.parametrize("x, s, f", [
    (10034.44, 7, 10034.446),
    (10034.44, 7, 10034.433)
    ])
def test_not_equals_SF_f(x, s, f):
    assert(si.SigFig.from_float(x, s) != f)

###############################################################
# Test < 
#
@pytest.mark.parametrize("x, s, y, t", [
    (3.14, 2, 3.16, 2),
    (10034.44, 7, 10034.45, 7),
    ])
def test_less_SF_SF(x, s, y, t):
    assert(si.SigFig.from_float(x, s) < si.SigFig.from_float(y,t))
    assert(si.SigFig.from_float(x, s) < y)


###############################################################
# __mult__ good 
#
@pytest.mark.parametrize("x, v, y", [
    (si.SigFig.from_float(10., 2), 30., si.SigFig.from_float(300., 2)),
    (si.SigFig.from_float(10., 2), si.SigFig.from_float(30., 3), si.SigFig.from_float(300., 2))
    ])
def test_mult_good(x, v, y):
    assert(x * v  == y) 

###############################################################
# __mult__ bad
#
@pytest.mark.parametrize("x, v, y", [
    (si.SigFig.from_float(10., 2), 30., si.SigFig.from_float(300., 3)),
    (si.SigFig.from_float(10., 2), si.SigFig.from_float(30., 3), si.SigFig.from_float(300., 3))
    ])
def test_mult_bad(x, v, y):
    assert(x * v != y) 

###############################################################
# __div__ good 
#
@pytest.mark.parametrize("x, v, y", [
    (si.SigFig.from_float(10., 2), 30., si.SigFig.from_float(300., 2)),
    (si.SigFig.from_float(10., 2), si.SigFig.from_float(30., 3), si.SigFig.from_float(300., 2))
    ])
def test_div_good(x, v, y):
    assert(y / v  == x) 

###############################################################
# __div__ bad
#
@pytest.mark.parametrize("x, v, y", [
    (si.SigFig.from_float(10., 2), 30., si.SigFig.from_float(300., 3)),
    (si.SigFig.from_float(10., 2), si.SigFig.from_float(30., 3), si.SigFig.from_float(300., 3)),
    (si.SigFig.from_float(10., 2), si.SigFig.from_float(30., 3), si.SigFig.from_float(300., 1))
    ])
def test_div_bad(x, v, y):
    assert(y / v != x) 


###############################################################
# __add__ good
@pytest.mark.parametrize("x, y, z", [
    (si.SigFig.from_float(1001.4, 5), si.SigFig.from_float(10.60, 4), si.SigFig.from_float(1012.0, 5)),
    (si.SigFig.from_float(1001.4, 5), 10.6, si.SigFig.from_float(1012.0, 5)),
    (si.SigFig.from_float(1001.4, 5), si.SigFig.from_float(10.60, 6), si.SigFig.from_float(1012.0, 5)),
    (si.SigFig.from_float(1001.4, 5), si.SigFig.from_float(10, 2), si.SigFig.from_float(1011, 4)),
    (si.SigFig.from_float(99.9, 3), si.SigFig.from_float(0.1, 1), si.SigFig.from_float(100.0, 4)),
    (si.SigFig.from_float(-1, 1), si.SigFig.from_float(1, 1), si.SigFig.from_float(0, 1))
    ])
def test_add_good(x, y, z):
    assert(x + y == z)

###############################################################
# __add__ dangerous
#
@pytest.mark.parametrize("x, y", [
    (si.SigFig.from_float(1, 1), si.SigFig.from_float(0.5, 1)),
    (si.SigFig.from_float(10, 2), si.SigFig.from_float(0.5, 1))
    ])
def test_add_bad(x, y):
    with pytest.warns(UserWarning) as w:
        a = x + y 

###############################################################
# __sub__ dangerous
#
@pytest.mark.parametrize("x, y", [
    (si.SigFig.from_float(1, 1), si.SigFig.from_float(0.5, 1)),
    (si.SigFig.from_float(10, 2), si.SigFig.from_float(0.5, 1))
    ])
def test_sub_bad(x, y):
    with pytest.warns(UserWarning) as w:
        a = x - y 

###############################################################
# __sub__ good
@pytest.mark.parametrize("x, y, z", [
    (si.SigFig.from_float(1001.4, 5), si.SigFig.from_float(10.6, 3), si.SigFig.from_float(1012.0, 5)),
    (si.SigFig.from_float(1001.4, 5), si.SigFig.from_float(10.60, 6), si.SigFig.from_float(1012.0, 5)),
    (si.SigFig.from_float(1001.4, 5), 10.60, si.SigFig.from_float(1012.0, 5)),
    (si.SigFig.from_float(1001, 4), si.SigFig.from_float(10, 2), si.SigFig.from_float(1011.4, 5)),
    (si.SigFig.from_float(99.9, 3), si.SigFig.from_float(0.1, 1), si.SigFig.from_float(100.0, 4)),
    (si.SigFig.from_float(-1, 1), si.SigFig.from_float(1, 1), si.SigFig.from_float(0, 1))
    ])
def test_sub_good(x, y, z):
    assert(x == z - y)

###############################################################
# test __str__ gives expected results
#
@pytest.mark.parametrize("x, y, st", [
    ( 1.2, 2, '1.2e+00'),
    (0.12, 2, '1.2e-01'),
    ( 12., 2, '1.2e+01')
])
#testing the string printing
def test_strings(x, y, st):
    assert(str(si.SigFig.from_float(x, y)) == st)

###############################################################
# from_float() should throw a warning here, since these values
# have dangerous precision issues
#
@pytest.mark.parametrize("x, y", [
    (10.5, 2),
    (-10.5, 2),
    (1.050e3, 2),
    (0.55, 1)
])
def test_rounding_warnings(x, y):
    with pytest.warns(UserWarning) as w:
        a = si.SigFig.from_float(value = x, sigfigs = y) #numerical precision can make this 10 or 11!

###############################################################
# - operator with dangerous results should throw warnings here, 
# but has safe constructions 
#
@pytest.mark.parametrize("x, y, a, b", [
    (1, 1, 0.5, 1),
    (0.5, 3, 1, 1),
])
def test_warning_on_sub(x, y, a, b):
    with pytest.warns(UserWarning) as w:
        z = si.SigFig.from_float(x, y) - si.SigFig.from_float(a, b) 

###############################################################
# + operator with dangerous results should throw warnings here, 
# but has safe constructions 
#
@pytest.mark.parametrize("x, y, a, b", [
    (1, 1, 0.5, 1),
])
def test_warning_on_add(x, y, a, b):
    with pytest.warns(UserWarning) as w:
        z = si.SigFig.from_float(x, y) + si.SigFig.from_float(a, b) 

################################################################
# w_round should throw a warning thanks to 
# dangerous rounding with machine precision
#
@pytest.mark.parametrize("x, y", [
    (10.5, 0),
    (-10.5, 0)
])
def test_w_round_warning(x, y):
    with pytest.warns(UserWarning) as w:
        a = si.w_round(x, y)

################################################################
# Cases where w_round should be identical to round
#
@pytest.mark.parametrize("x, y", [
    (10.234,  3),
    (10.234,  2),
    (10.234,  1),
    (10.234,  0),
    (10.234, -1),
    (10.234, -2)
    ])
def test_w_round(x, y):
    assert si.w_round(x, y) == round(x, y) 
         
################################################################
# this should NOT throw a warning since this is a safe rounding
#
@pytest.mark.filterwarnings("error")
@pytest.mark.parametrize("x, y", [
    (10.9, 1),
    (10.8, 1),
    (10.7, 1),
    (10.6, 1),
    (10.4, 1),
    (10.3, 1),
    (10.2, 1),
    (10.1, 1),
])
def test_no_warining(x, y):
    a = si.SigFig.from_float(value = x, sigfigs = y) 
    
################################################################
# Test the absoulte value funciton
@pytest.mark.parametrize("x, y", [
    (si.SigFig.from_float(-1.0, 1), si.SigFig.from_float(1.0, 1))
    ])
def test_abs_good(x, y):
    assert(abs(x) == y)
