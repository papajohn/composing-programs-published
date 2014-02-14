"""Newton's method, applied to single term polynomials with coefficient 1 to
compute nth roots.
"""

def improve(update, close, guess=1):
    while not close(guess):
        guess = update(guess)
    return guess

def approx_eq(x, y, tolerance=1e-3):
    return abs(x - y) < tolerance

def square_root(a):
    """Return the square root of a, computed by Newton's method.

    >>> square_root(4)
    2.0000000929222947
    >>> square_root(64)
    8.000001655289593
    >>> square_root(2)
    1.4142156862745099
    """
    def f(x):
        return x * x - a
    def df(x):
        return 2 * x
    return find_zero(f, df)

def nth_root(n, a):
    return find_zero_of_x_to_the_n_minus_a(n, a)

def power(x, n):
    """Return x * x * x * ... * x for x repeated n times.

    >>> power(2, 3)
    8
    >>> power(4, 5)
    1024
    >>> power(6, 0)
    1
    """
    product, num_xs = 1, 0
    while num_xs < n:
        product, num_xs = product * x, num_xs + 1
    return product

def find_zero_of_x_to_the_n_minus_a(n, a):
    """Return x such that x^n - a = 0.

    >>> find_zero_of_x_to_the_n_minus_a(2, 64)
    8.000001655289593
    >>> find_zero_of_x_to_the_n_minus_a(3, 64)
    4.000017449510739
    >>> find_zero_of_x_to_the_n_minus_a(6, 64)
    2.000000032935665
    """
    def f(x):
        return power(x, n) - a
    def df(x):
        return n * power(x, n-1)
    return find_zero(f, df)

def newton_update(f, df):
    def update(x):
        return x - f(x) / df(x)
    return update

def find_zero(f, df):
    """Return a zero of differentiable f with derivative df."""
    def near_zero(x):
        return approx_eq(f(x), 0)
    return improve(newton_update(f, df), near_zero)
