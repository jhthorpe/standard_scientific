# test_float_compare.py
#
# Pytests for checking the behavior of float_compare

import pytest

import standard_scientific as si

##
# These are the same 
@pytest.mark.parametrize("x, y", [
    (1., 1.),
    (1.234e23, 1.234e23),
    (1.234e-23, 1.234e-23),
    ])
def test_equal_good(x, y):
    assert(si.equal_floats(x, y))

##
# These are not the same
@pytest.mark.parametrize("x, y", [
    (1., 2.),
    (1.23e-23, 1.234e-23),
    (-1.234e23, 1.234e23)
    ])
def test_not_equal(x, y):
    assert(not si.equal_floats(x, y))

##
# These are the same when they should "not" be! 
#
# expected unexpected behavior
@pytest.mark.parametrize("x, y", [
    (1., 1. + si.eps),
    (1.e20, 1.e20 * (1. + si.eps))
    ])
def test_equal_surprise(x, y):
    assert(si.equal_floats(x, y))

##
# These are different when they should not be!
#  
# expected unexpected behavior
#
@pytest.mark.parametrize("x, y", [
    (0., 0.)
    ])
def test_not_equal_surprise(x, y):
    assert(not si.equal_floats(x, y))
