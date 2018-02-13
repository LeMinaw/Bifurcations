from math import exp, log, cos, sin
from random import random, choice

white_to_black = {'c_min':(0,   0,   0),   'c_max':(255, 255, 255)}
blue_to_red    = {'c_min':(0,   0,   255), 'c_max':(255, 0,   0)}
cyan_to_red    = {'c_min':(0,   255,  255), 'c_max':(255, 0,   0)}
black_to_red   = {'c_min':(0,   0,   0),   'c_max':(255, 0,   0)}
red_to_black   = {'c_min':(255,   0,   0), 'c_max':(0,   0,   0)}

def namefile(string):
    chars = ((' ', ''), ('*', ''), ("'", ''))
    string = str(string)
    for old, new in chars:
        string = string.replace(old, new)
    return string

def clamp(x, inf=0, sup=1):
    return min(sup, max(inf, x))

def linInterp(x, xMin=0, xMax=1, yMin=0, yMax=1):
    return (x - xMin) * (yMax - yMin) / (xMax - xMin) + yMin

def uid(n=5):
    strs = ('lou', 'da', 'cris', 'ker', 'nel', 'li', 'nux')
    if n == 0:
        return ''
    return choice(strs) + uid(n - 1)

def rev_enumerate(iterable):
   for i in reversed(range(len(iterable))):
      yield i, iterable[i]

def approxIndex(iterable, item, threshold):
    for i, iterableItem in rev_enumerate(iterable):
        if abs(iterableItem - item) < threshold:
            return i
    return None

def gen_cmap(x_min, x_max, c_min, c_max):
    def cmap(x):
        return tuple(int(linInterp(x, x_min, x_max, c_min[i], c_max[i])) for i in range(3))
        return tuple(min(c_max[i], max(c_min[i], int(linInterp(x, x_min, x_max, c_min[i], c_max[i])))) for i in range(3))
    return cmap


class Population:
    def __init__(self, fertility, initial=.5):
        self.fertility = fertility
        self.initial = initial

    def generator(self, iterations):
        for i in range(iterations):
            if i == 0:
                pop = self.initial
            else:
                try:
                    fertility = self.fertility[i % len(self.fertility)]
                except TypeError:
                    fertility = self.fertility
                pop = fertility * pop * (1 - pop)
                # pop = fertility * (sin(pop)+1)/2
            yield pop

    def get_loop_values(self, threshold=.000001, max_iteration=10000):
        lastPops = []
        for pop in self.generator(max_iteration):
            index = approxIndex(lastPops, pop, threshold)
            if index:
                return lastPops[index:]
            lastPops.append(pop)

    def get_first_values(self, iterations=5000):
        pops = []
        for pop in self.generator(iterations):
            if pop in pops[-10:]:
                break
            pops.append(pop)
        return pops[len(self.fertility):] # Truncation removes continuous h lines (=start values), not sure why however


class DoublePopulation(Population):
    def __init__(self, f1, f2, a, i1=.5, i2=.5):
        self.f1, self.f2 = f1, f2
        self.i1, self.i2 = i1, i2
        self.a = a

    def generator(self, iterations):
        for i in range(iterations):
            if i == 0:
                pop1 = self.i1
                pop2 = self.i2
            else:
                pop1 = self.f1 * pop1 * (1 - (pop1 - self.a * pop2))
                pop2 = self.f2 * pop2 * (1 - (pop2 + self.a * pop1))
            yield (pop1, pop2)

    def get_first_values(self, iterations=5000):
        pops = []
        for pop in self.generator(iterations):
            if pop in pops[-10:]:
                break
            pops.append(pop)
        return pops[1:]


class Bifurcation:
    def __init__(self, fertilities=('i'), iterations=2000):
        self.fertilities = fertilities
        self.iterations  = iterations

    @property
    def max_fertility(self):
        return max([eval(x, {'i':1}) if type(x) is str else x for x in self.fertilities])

    def render(self, x_min=0, x_max=4, x_precision=2000, y_precision=2000, cmap_colors=white_to_black):
        from PIL import Image
        from colorsys import yiq_to_rgb, hls_to_rgb

        if x_min > x_max:
            raise ValueError("be sure x_max > x_min")

        start = int(x_min * x_precision)
        end   = int(x_max * x_precision)
        # end   = int(x_max * x_precision // self.max_fertility)
        size = end - start

        img = Image.new('RGB', (size, y_precision*20), "white")
        pixels = img.load()
        cmap = gen_cmap(0, self.iterations / 2, **cmap_colors)

        for i in range(start, end):
            if i % (size // 100) == 0:
                print("{0}/{1} ({2:.0f}%)".format(i - start, size, (i - start) / size * 100))
            i = i / x_precision
            # fertilities = [eval(x, {'i': i}) if type(x) is str else x for x in self.fertilities] # Evaluates any string in fertilities
            # pop = Population(fertilities)
            pop = DoublePopulation(i, .4, .9)
            values = pop.get_first_values(self.iterations)
            if values is not None:
                for index, value in enumerate(values):
                    # j = y_precision * (1 - int(value)) - 1 # Otherwise y axis is upside-down
                    # j = int(y_precision * value)
                    j0 = int(y_precision * value[0])
                    j1 = int(y_precision * value[1])
                    try:
                        # pixels[i * x_precision - start, j] = cmap(index)
                        pixels[i * x_precision - start, j0 + y_precision*] = (255, 0, 0)
                        pixels[i * x_precision - start, j1 + y_precision] = (0, 0, 255)
                    except IndexError:
                        print("(%s,%s:%s) is out of range" % (i * x_precision - start, j0, j1))
                        break
                        raise IndexError("(%s,%s) is out of range" % (i * x_precision - start, j))
        return img

if __name__ == '__main__':
    bif = Bifurcation(('i', 3.7, 'i', 3.9), 600)
    args = {
        'x_min': 0,
        'x_max': 4,
        'x_precision': 2000,
        'y_precision': 2000,
        'cmap_colors': red_to_black
    }
    bif.render(**args).save('%s-%s-test.png' % (namefile(bif.fertilities), bif.iterations))
