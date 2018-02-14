"""This module is composed of function definitions describing recurrent population evolution.
Each function takes 3 args:
- pop: Population at previous state
- fertility: Fertility value, likely positive
- environment: Ponderated changes in population, eg. predation. Must default to 0, and can be either positive or negative."""

from utils import clamp
from math  import sin

def logistic(pop=.5, fertility=1, environment=0):
    """Logistic equation.
    fp(1-p) = -fp^2 + fp"""
    return fertility * pop * (1 - pop)

def logistic_env_product(pop=.5, fertility=1, environment=0):
    """Tweaked version of the logistic function, taking environment into account by multiplicating population.
     fp(1-p)e = -fep^2 + fep"""
    return logistic(pop, fertility) * environment
    # return fertility * pop * (1 - pop) * environment

def logistic_env_fert(pop=.5, fertility=1, environment=0):
    """Tweaked version of the logistic function, taking environment into account by modifying fertility.
    (f+e)p(1-p) = -(f+e)p^2 + (f+e)p"""
    return logistic(pop, fertility + environment)
    # return (fertility + environment) * pop * (1 - pop)

def lotka_volterra(pop=.5, fertility=1, environment=0):
    """Competitive Lotka–Volterra equation.
    fp(1-p+e) = -fp^2 + f(1+e)p"""
    return fertility * pop * (1 - pop + environment)

def trigonometric(pop=.5, fertility=1, environment=0):
    """Returns the next rank of a strange sin based function."""
    return fertility * (sin(pop + environment) + 1) / 5
