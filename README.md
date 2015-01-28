# discrete_differentiator
Takes a series of equally spaced points, and computes the point-wise derivative.

Takes a sequence of numbers, and returns a sequence of numbers 
that are the derivative of the given sample. Takes the sequence
either as a Python array, or in a CSV file. Differentiation is
done as follows:

	For first data point uses:        f'(x) =(-f(x+2h) + 4*f(x+h) - 3*f(x))/(2h)
	For internal data points uses:    f'(x) =(f(x+h) - f(x-h))/(2h)
	For last data point uses:         f'(x) =(f(x-2h)  - 4*f(x-h) + 3*f(x))/(2h)

Accommodates CSV files with multiple columns, of which one is
contains the sequence to differentiate. Accommodates CSV files
with or without column header.


