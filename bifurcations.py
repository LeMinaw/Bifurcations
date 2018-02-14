"""This module contains stuff for generating bifurcation diagrams."""

from PIL       import Image
from utils     import replace_patterns, lin_interp
from colormaps import black, blue_to_black, red_to_black, orange_to_black

class Diagram:
    """This class represents a statistial states diagram (such as bifurcation diagrams)."""

    def __init__(self, system, y_min=0, y_max=4, width=1920, height=1080, colormaps=black):
        """Creates a new diagram.
        - system: PopulationSystem to be plotted
        - y_min: Horizontal axis value where the plotting starts
        - y_max: Horizontal axis value where the plotting ends
        - width: Plot width in px
        - height: Plot height in px
        - cmaps: Sequence of color maps for each Population of the PopulationSystem.
        If a single color map is provided, all Populations will share it."""
        self.system = system
        self.y_min, self.y_max  = y_min, y_max
        self.width, self.height = width, height
        self.colormaps   = colormaps

    @property
    def colormaps(self):
        return self.__colormaps

    @colormaps.setter
    def colormaps(self, cmaps):
        if type(cmaps) is ColorMap:
            cmaps = (cmaps,) * len(self.system.populations)
        self.__colormaps = cmaps

    def __str__(self):
        """Simple informal string representation for this Diagram."""
        return "%s on [%s, %s]" % (self.system, self.y_min, self.y_max)

    def gen_file_name(self):
        """Generates a convenient file name."""
        patterns = ((":", ''), ("*", ''), ("'", ''))
        return '%s.png' % replace_patterns(str(self), patterns)

    def render(self, path=None, filename=None):
        """Renders the Diagram and returns it.
        - path: If specified, saves the image file to this path."""

        img = Image.new('RGB', (self.width, self.height), "white")
        pixels = img.load()

        max_fert_len = self.system.get_max_fert_len()
        for pix_y in range(self.width):
            y = lin_interp(pix_y, 0, self.width, self.y_min, self.y_max)
            self.system.y = y

            # percent = pix_y / self.width * 100
            # if percent % 1 == 0:
            #     print("{}/{} ({:.0f}%)".format(pix_y, self.width, percent))

            for state_index, state in enumerate(self.system.get_first_states()):
                if state_index <= max_fert_len: # This avoids continuous y=k type lines on the graph by not showing very first values
                    continue

                for pop_index, value in enumerate(state):
                    pix_x = int(lin_interp(value, 0, 1, 0, self.height - 1))
                    cmap = self.colormaps[pop_index]
                    pix_color = cmap(state_index, 0, self.system.iterations / 2)
                    try:
                        pixels[pix_y, pix_x] = pix_color
                    except IndexError:
                        print("Out of range: (%s:%s)" % (pix_y, pix_x))

        if path is not None or filename is not None:
            if filename is None:
                filename = self.gen_file_name()
            if path is None:
                path = ''
            print("Now saving %s..." % filename)
            img.save(path + filename)

        return img

if __name__ == '__main__':
    from populations     import Population, PopulationSystem
    from multiprocessing import Pool
    import laws

    y = lambda y, i: y
    pop_1 = Population(laws.logistic_env, [y])
    pop_2 = Population(laws.logistic_env, [y])
    pop_3 = Population(laws.logistic_env, [y])

    sys = PopulationSystem({
        pop_1: {            pop_2:  2, pop_3: -2},
        pop_2: {pop_1: -2,             pop_3:  2},
        pop_3: {pop_2:  2, pop_2: -2}
    }, iterations=400) # iterations = 0.3 * height

    diag = Diagram(sys, y_min=0, y_max=4, width=1920, height=1080, colormaps=[red_to_black, blue_to_black, orange_to_black])
    diag.render().show()
