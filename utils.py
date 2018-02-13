"""Various and generic stuff."""

from inspect import getsource
from math    import log, e
import re

def clamp(x, inf=0, sup=1):
    """Clamps x in the range [inf, sup]."""
    return inf if x < inf else sup if x > sup else x

def replace_patterns(string, patterns):
    """Replaces multiple patterns in a string.
    - patterns: Sequence of (old, new) substrings."""
    for old, new in patterns:
        string = string.replace(old, new)
    return string

def lin_interp(x, x_min=0, x_max=1, y_min=0, y_max=1):
    """Lineary interpolates x from the range [x_min, xmax] to the range [y_min, y_max]."""
    return (x - x_min) * (y_max - y_min) / (x_max - x_min) + y_min

def pow_interp(x, power=.5, x_min=0, x_max=1, y_min=0, y_max=1):
    """Interpolates x according to a power low, from the range [x_min, xmax] to the range [y_min, y_max]."""
    return lin_interp(lin_interp(x, x_min, x_max)**power, 0, 1, y_min, y_max)

def log_interp(x, x_min=0, x_max=1, y_min=0, y_max=1):
    """Interpolates x according to a logarithmic law, from the range [x_min, xmax] to the range [y_min, y_max]."""
    return lin_interp(log(lin_interp(x, x_min, x_max) + 1), 0, log(2), y_min, y_max)

def rev_enumerate(iterable):
    """Enumerates an iterable object in reverse. Original indexes are preserved."""
    for i in reversed(range(len(iterable))):
        yield i, iterable[i]

def approxIndex(iterable, item, threshold):
    """Same as the python index() function but with a threshold from wich values are considerated equal."""
    for i, iterableItem in rev_enumerate(iterable):
        if abs(iterableItem - item) < threshold:
            return i
    return None

def is_sequence(item):
    """Returns True if an object is iterable."""
    return hasattr(type(item), '__iter__')

def get_lambda_code(lmbd, n=0):
    """Dirty way to get the code of a lambda function."""
    lmbd = getsource(lmbd)
    pat = r"lambda.*?:\s?(.*?)[\]\n\,]"
    matches = re.findall(pat, lmbd)
    return matches[n]

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    x = range(500)
    y = range(1000)
    plt.plot([pow_interp(n, .5, 0, 500,  0, 10) for n in x], label="Power 1/2 interpolation")
    plt.plot([pow_interp(n,  2, 0, 500,  0, 10) for n in x], label="Power 2 interpolation")
    plt.plot([pow_interp(n, .5, 0, 1000, 0, 10) for n in y], label="Power 1/2 interpolation")
    plt.plot([pow_interp(n,  2, 0, 1000, 0, 10) for n in y], label="Power 2 interpolation")
    plt.plot([log_interp(n,     0, 500,  0, 10) for n in x], label="Log interpolation")
    plt.plot([log_interp(n,     0, 1000, 0, 10) for n in y], label="Log interpolation")
    plt.legend()
    plt.show()
