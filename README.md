# standard_scientific 
Package that facilitates the representation and interpretation of data in scientific notation. The main features are two classes, the `SigFig` class and the `SciData` class.  

## `SigFig`
This class is used to represent data with significant figures, and supports the usual operations (+,-,\*,/) with rules in place that ensure the correct number of figures in the result. It should be noted that the constructors generated by @dataclass should NOT be trusted to generate true "sigfigs", since they are just copying data. To generate a sigfig, it is *strongly* recommended that you use the `from_float` function to specify the value and the number of significant figures you want it to have. For instance, the following operations proceed correctly:
```
import standard_scientific as si
a = si.SigFig.from_float(99.9001, 3) #99.9 with 3 sig figs
b = si.SigFig.from_float(0.1, 2) #0.1 with 1 sig fig
a + b == si.SigFig.from_float(1e3, 4), #100.0 with 4 sig figs
```
Where the number of sig figs passed in are used to round the provided value to the correct number of digits (with an important exception discussed below)

###A Note on SigFig Comparison. i
Comparison of floating point numbers is inherently a dangerous and complicated process. The inclusion of Significant Figures simplifies this process to some extent, as it provides a rigerous description of exactly which places in a number can be considered, which, *generally*, is far fewer places than significant figures in floating point (double precision) numbers. *However*, there are still edge cases that can be the source of frustration. Take for example the following code snippit:

```
x = si.SigFig.from_float(value = 1.5, sigfigs = 1) #Does this round to 1 or 2?
``` 

The obvious problem is that this exact scenario is a grey zone in the practical implementation of significant figures, the problem being that 1.5 is not actually 1.5 (exactly 3/2), but rather float(1.5), which comes with questions of machine precision. In this case we can resolve the problem by taking the rounding out of the hands of the SigFig class, and instead using `x = si.SigFig(value = 2, sigfigs = 1)`. However, a more insidious problem arrises when:

```
x = si.SigFig.from_float(value = 1, sigfigs = 1)
y = si.SigFig.from_float(value = 0.50, sigfigs = 2)
z = x - y #will this be 1 or 0?? 
```

where we encounter the strange situation that 1 - 0.50 might, in fact, be either 1 or 0 *depending on the machine noise of the difference in the values*, and that either result *should* be considered as different values in significant figures! This is a natural consequence of the issues comparing floating point number (for a better description, see *https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/*). This problem is somewhat alleviated when uncertainties are provided with the given value, but in the SigFigs class we must settle for providing the user with a warning when it detects the rounding in the `from_float` constructor is sensitive to noise. For you precision nerds out there, this is currently implemented as a check that  `x + x*eps` and `x - x*eps` round to the same SigFig, and the comparison between SigFigs is implemented as a check that they differ by less than 0.5 in the last significant digit.  

## `SciData`
Under construction.

## Requirements
    * pytest
    * python3.0 or later
    * numpy

## Installation
    `python3 -m pip install .`

Testing provided by executing `pytest -W error` within the tests directory. 

## Import
    `import standard_scientific as si`


