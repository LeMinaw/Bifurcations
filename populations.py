"""This module contains stuff for representation and computation of concurrent population models."""

from dill.source import getsource
from random      import seed, choice, randint
from utils       import replace_patterns, get_lambda_code, is_sequence

class Population:
    """This class represents a single population."""

    def __init__(self, law, fertilities=lambda y, i: y, initial=.5):
        """Creates a new Population.
        - law: Callable describing reccurent population evolution (see PopulationLaw class).
        - fertilities : A sequence specifing the fertility cycle of the population.
        Fallback will be provided for single values. The fertility can be a value or a callable.
        Other functions of this module will evaluate it with parameters (y, i), where y is horizontal axis coords and i the current iteration index.
        - initial: Initial population value."""
        self.law         = law
        self.fertilities = fertilities
        self.initial     = initial
        self.footprint = law.__name__ + str(fertilities) + str(initial)
        self.name()

    @property
    def fertilities(self):
        return self.__fertilities

    @fertilities.setter
    def fertilities(self, ferts):
        if not is_sequence(ferts):
            ferts = (ferts,)
        self.__fertilities = tuple(ferts)

    def __str__(self):
        """Non-precise string representation."""
        ferts = ()
        for fert in self.fertilities:
            if callable(fert):
                ferts += (get_lambda_code(fert, len(ferts)),)
            else:
                ferts += (fert,)
        return "{} ({}:{})".format(self.name, self.law.__name__, ferts)

    def name(self):
        """Simple concatenation fonction for generating random population names."""
        strs = ('lou', 'da', 'cris', 'ker', 'nel', 'li', 'nux', 'py', 'thon')
        seed(self.footprint)
        self.name = ''.join([choice(strs) for i in range(randint(1, 4))])


class PopulationSystem:
    """Represents a system of several population and the relation they have."""

    def __init__(self, populations, iterations=1000):
        """Creates a new PopulationSystem.
        - population: Can either be a sequence containing Population objects,
        or a dict formatted as follows, describing populations and relations at once.
        {
            pop_1: {            pop_2: 0.5, pop_3: -0.9},
            pop_2: {pop_1: 0.1,                        },
            pop_3: {pop_1: 0.9, pop_2:-1               }
        }
        In this exemple, pop_2 presence will make pop_1 grow by a factor of 0.5, but pop_3 presence will decrease it by a factor 0.9.
        Relations are generally (but not necessarily) symmetrical. Here, pop_3 and pop_1 are symetrically related, but pop_1 and pop_2 are not.
        This is useful for modelisation of symbiotic mechanisms.
        If a population is not affected by another, you can likewise set a relation of factor 0 or omit it completely.
        Here, pop2 is not affected by pop3 presence.
        Circular references (a relation between a population and itself) are not allowed.
        - iterations: The number of states of the system to be computed."""
        self.populations = populations
        self.iterations  = iterations
        self.y = 0

    @property
    def populations(self):
        return self.__populations

    @populations.setter
    def populations(self, pops):
        if type(pops) is not dict:
            pops = {pop: {} for pop in pops}
        else:
            for pop, relations in pops:
                if pop in relations:
                    raise ValueError("A population cannot be in relation with itself. Use population's fertility for that.")
        self.__populations = pops

    def get_max_fert_len(self):
        return max([len(pop.fertilities) for pop in self.populations])

    def __str__(self):
        """Simple informal string representation."""
        return ' ; '.join([str(pop) for pop in self.populations])

    def __iter__(self):
        """Inits iteration."""
        self.i = 0
        self.state = {pop: pop.initial for pop in self.populations}
        return self

    def __next__(self):
        """Computes next system state. Iteration number is set in __init__."""
        if self.i > self.iterations:
            raise StopIteration
        if self.i > 0:
            next_state = {}
            for pop, relations in self.populations.items():
                fertility = pop.fertilities[self.i % len(pop.fertilities)]
                if callable(fertility):
                    fertility = fertility(self.y, self.i)
                environment = sum([self.state[related_pop] * relation for related_pop, relation in relations.items()])
                next_state[pop] = pop.law(self.state[pop], fertility, environment)
            self.state = next_state
        self.i += 1
        return tuple(self.state.values())

    def get_first_states(self, max_loop_size=10, thresh=.000001):
        """Returns system states until a loop or a single convergence point is detected in the values.
        This function does NOT return proper population data, but is intended to shortcut things for faster generation.
        - max_loop_size: The maximum loop size that can be detected.
        Big values can sometimes save time by shortcuting computation, but will add overhead checking for loops.
        - thresh: The threshold at two value will be considerated equals.
        Big values saves time by detecting asymptotic behaviours faster but reduces accuracy."""
        states = ()
        for state in self:
            if len(states) > 1 and all([abs(state[i] - states[-1][i]) < thresh for i in range(len(state))]):
                break
            if state in reversed(states[-max_loop_size:-1]):
                break
            states += (state,)
            yield state

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import laws

    pop_1 = Population(laws.logistic,      [2.5, 2.1])
    pop_2 = Population(laws.trigonometric, [2.5, 2.1])
    system = PopulationSystem({
        pop_1: {pop_2:  .5},
        pop_2: {pop_1: -.5}
    }, iterations = 100)

    a, b = [], []
    for state in system:
        a.append(state[0])
        b.append(state[1])
    plt.plot(a, label=str(pop_1))
    plt.plot(b, label=str(pop_2))
    plt.legend()
    plt.show()
