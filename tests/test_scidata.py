# test_scidata.py
#
# Provides interface with Pytest for testing the SciData class
# and related functionality

import pytest

import standard_scientific as si 

###############################################################
# Test == comparison
#
@pytest.mark.parametrize("a, b", [
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), None, None, True),
      si.SciData(si.SigFig.from_float(12.345, 5), None, None, True)) 
    ])
def test_comparison_good(a, b):
    assert(a == b)

###############################################################
# Test != comparison
#
@pytest.mark.parametrize("a, b", [
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), True)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.5e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 3), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.068, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 3), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.346, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 6), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
    ])
def test_comparison_good(a, b):
    assert(a != b)


################################################
# Test generation of SciData fs
#
@pytest.mark.parametrize("v, u, r, ex, c", [
    (           si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False, 
     si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False) ),
    (           si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2),  True, 
     si.SciData(si.SigFig.from_float(12.345, 5),                           None,                            None,  True) ),
    (           si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2),                            None, False, 
     si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False) )
    ])
def test_from_SigFig_good(v, u, r, ex, c):
    assert(si.SciData.from_SigFigs(value = v, unc = u, rel_unc = r, is_exact = ex) == c)


################################################
# Test that we get assertion problems from the following 
#
@pytest.mark.parametrize("v, u, r, ex", [
    (si.SigFig.from_float(12.345, 5),                           None, si.SigFig.from_float(5.4e-3, 2), False), 
    (                           None, si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False), 
    (                           None, si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), True), 
    ])
def test_from_SigFig_bad(v, u, r, ex):
    with pytest.raises(Exception) as e:
        si.SciData.from_SigFigs(value = v, unc = u, rel_unc = r, is_exact = ex) 

'''
###############################################################
# Check that there is an error if we give bad input 
#
@pytest.mark.parametrize("x", [
    (None),
    ('abc')
])
def test_exponent_from_float_excpetions(x):
    with pytest.raises(Exception) as e:
        si.exponent_from_float(x)
'''
