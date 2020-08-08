from math import factorial

def prod(iterable,*, start=1):
    """
    Returns product of all values in iterable, starting at start
    """
    for i in iterable:
        start*= i
    return start

def perm(n, r=None):
    """
    nPr function.
    """
    # Setting r to n for bad values
    if r is None:
        r = n
        
    # Return for non-ints
    if not isinstance(n, int):
        raise TypeError('must be a nonzero integer value, not ' + str(type(n)))
    if not isinstance(r, int):
        raise TypeError('must be a nonzero integer value, not ' + str(type(r)))
        
    # Return for negatives
    if n < 0 or r < 0:
        raise ValueError('must be a nonzero integer value')
    
    # Return if r > n
    if r > n:
        return 0
    
    # Returns
    return factorial(n) / factorial(n - r)

def comb(n, r=None):
    """
    nCr function.
    Simple modification of perm function.
    """
    if r is None:
        r = n
    return perm(n, r) / factorial(r)
