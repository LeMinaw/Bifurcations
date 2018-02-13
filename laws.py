"""This module is composed of function definitions describing recurrent population evolution.
Each function takes 3 args:
- pop: Population at previous state
- fertility: Fertility value, likely positive
- environment: Ponderated changes in population, eg. predation. Must default to 0, and can be either positive or negative."""

from utils import clamp
from math  import sin

def logistic(pop, fertility, environment=0):
    """Returns the next rank of the discrete logistic function."""
    return fertility * pop * (1 - pop + environment)

def logistic_clamp(pop, fertility, environment=0):
    """Clamped version of the logistic function."""
    return clamp(fertility * pop * (1 - pop + environment))

def trigonometric(pop, fertility, environment=0):
    """Returns the next rank of a strange sin based function."""
    return fertility * (sin(pop + environment) + 1) / 5
