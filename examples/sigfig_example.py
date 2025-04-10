import standard_scientific as si

# Create a significant figure from a float, rounded to the correct number of decimal places
x = si.SigFig.from_float(value = 101.1, sigfigs = 4)
y = si.SigFig.from_float(value = 1.1, sigfigs = 1)
z = si.SigFig.from_float(value = -2.000, sigfigs = 5)

print("x = ", x)
print("y = ", y)
print("z = ", z)

# You can access useful things as so:
print("x value = ", x.value)
print("x sigfigs = ", x.sigfigs)
print("x exponent = ", x.exponent)

# There is also a useful (though expensive) operation to return the "true" exponent of a number in 
# scientific notation
print("True exponent of 12.3 is", si.exponent_from_float(12.3))

# This one will issue a warning thanks to the sensitivity of the resulting sigfig caused by numerical precision 
print("You should see some warning after this message!")
a_dangerous = si.SigFig.from_float(value = 0.15, sigfigs = 1)

# You can access what epsilon is used in the standard_scientific numerical stability checks
print("epsilon used in standard_scientic is", si.eps)

# We can perform some comparison operations...
print(" x =? y", x == y)
print(" x >? y", x > y)

# ... and also some basic arithmatic, the results of which are sigfigs. Raw values
# are taken to be "exact" (infinite number of sigfigs).
xpy = x + y
print("x + y = ", xpy)
print("x + y.value = ", x + y.value)

print("x * y = ", x * y)
print("x * y.value = ", x * y.value)

# Some other supported functions
print("Absolute value of z is ", abs(z))

