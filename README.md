# discrete_differentiator
Takes a series of equally spaced points, and computes the point-wise derivative.

Takes a sequence of numbers, and returns a sequence of numbers 
that are the derivative of the given sample.

The sequence may either be a Python array, or available in a CSV
file. Differentiation is done as follows:

	For first data point uses:        f'(x) =(-f(x+2h) + 4*f(x+h) - 3*f(x))/(2h)
	For internal data points uses:    f'(x) =(f(x+h) - f(x-h))/(2h)
	For last data point uses:         f'(x) =(f(x-2h)  - 4*f(x-h) + 3*f(x))/(2h)

Accommodates CSV files with or without column header. Also
accommodates CSV files with multiple columns, of which one contains
the sequence to differentiate.

Despite many parameters, simple cases are simple. Examples:

    from discrete_differentiator.discrete_differentiator import DiscreteDifferentiator as DD

    o DD.differentiate([2,4,6,7])
    o Given a csv file foo.csv with a single column of numbers:
       DD.differentiate('foo.txt')
    o A csv file like this:
         "trash column", 10
         "more trash", 20
       DD.differentiate('foo.txt', colIndex=1)

See test file for more examples.

