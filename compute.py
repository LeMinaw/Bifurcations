# from multiprocess    import Pool
from bifurcations    import Diagram, red_to_black
from populations     import Population, PopulationSystem
from utils           import lin_interp, pow_interp
from time            import clock
from argparse        import ArgumentParser
import laws

START   = 2.5
END     = 4.0
FRAMES  = 800
THREADS = 8 # Must be a divisor of FRAMES

ap = ArgumentParser()
ap.add_argument("-c", "--core",    required=False, default='0', help="core number for this thread")
args = vars(ap.parse_args())
core = int(args['core'])

def compute_frame(frame):
    timer = clock()
    print("Starting computation of frame %s/%s" % (frame, FRAMES))

    # k = lin_interp(frame, 0, FRAMES, START, END)
    k = pow_interp(frame, 0.3, 0, FRAMES, START,  END)

    y = lambda y, i: y
    pop = Population(laws.logistic, [y, y, k, k])
    sys = PopulationSystem([pop], iterations=600)
    diag = Diagram(sys, width=1920*2, height=1080*2, colormaps=[red_to_black])
    diag.render(filename="soo-{:04d}.png".format(frame))

    print("Done frame {}/{} ({:.2f}s)".format(frame, FRAMES, clock() - timer))
    return None


if __name__ == "__main__":
    start_frame = int((FRAMES / THREADS) * core)
    end_frame   = int((FRAMES / THREADS) * (core + 1))

    for frame in range(start_frame, end_frame):
        compute_frame(frame)
    # with Pool(processes=THREADS) as pool:
    #     pool.map(compute_frame, range(FRAMES))
    exit()
