"""A basic particle simulator that simulates a short-range 1/r^2 repulsive force
between particles in an enclosed 2D space. Uses an O(n^2) all-to-all algorithm.
Supports multithreading, multiprocessing, and graphical visualization.

Usage: python3 particle.py [-t <num_threads>] [-p <num_processes]
           [-n <num_particles>] [-s <num_steps>] [-v] [-g]
           [-u <update_interval>] [-dt <step_length>]

The -t flag enables multithreading, with the given number of threads.
The -p flag enables multiprocessing, with the given number of processes.
(This code does not currently support combining multithreading and
multiprocessing.)
The -n flag simulates the given number of particles; default is 20.
The -s flag simulates for the given number of steps; default is 1000.
The -v and -g flags enable visualization, updating after every step.
The -u flag enables visualization, updating after the given number of steps.
The -dt flag sets the length of a timestep; default is 0.0005. Long-running
simulations should decrease this to avoid blowup due to discretization effects.
The -e flag enables energy normalization, which normalizes energy in each
timestep to match the initial energy. This also avoids blowup.

This code is based on the particle simulation project in CS267 at UC Berkeley.
Visualization uses John Zelle's Python graphics library
(http://mcsp.wartburg.edu/zelle/python/).
"""

from random import random, seed, shuffle
from math import ceil, sqrt
from functools import reduce
from time import time
from ucb import main
import threading, multiprocessing
import graphics
import sys

default_num_particles = 20
default_steps = 1000
colors = ['blue', 'orange', 'red', 'green', 'brown', 'purple', 'cyan', 'black']

###########################
# Particle Representation #
###########################

class Particle(object):
    """Representation of a single particle in the simulation. A particle has a
    2D position, velocity, and acceleration, and interacts with other nearby
    particles. In this simulation, all particles have the same mass. Particles
    also maintain their graphical representation in the visualization."""
    density = 0.0005
    mass = 0.01
    cutoff = 0.01
    # prevent very large forces due to discretization/fp inaccuracy
    min_r2 = (cutoff / 100) ** 2
    dt = 0.0005
    box_size = None
    scale_pos = None
    next_id = 0
    energy_correction = 1 # energy normalization

    def __init__(self, x, y, vx, vy, ax, ay):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.id = Particle.next_id
        Particle.next_id += 1
        self.graphic = None

    def init_graphic(self, win, rad, owner=None):
        """Create a graphical representation of this particle for visualization.
        win is the graphics windown in which the particle should be drawn, rad
        is the radius of the particle, and owner is the thread/process number of
        the thread that owns this particle."""
        p = graphics.Point(self.x * self.scale_pos + rad + 5,
                           self.y * self.scale_pos + rad + 5)
        self.graphic = graphics.Circle(p, rad)
        color = colors[owner % len(colors)] if owner is not None else 'blue'
        self.graphic.setOutline(color)
        self.graphic.setFill(color)
        self.graphic.draw(win)

    def apply_force(self, other):
        """Apply a simple short range repulsive force from another particle on
        this particle."""
        return self.apply_force_from_coords(other.x, other.y)

    def apply_force_from_coords(self, ox, oy):
        """Apply a simple short range repulsive force from a particle at
        the given coordinates on this particle."""
        dx = ox - self.x
        dy = oy - self.y
        if dx == dy == 0:
            return # no directional force from particle at same location
        r2 = max(dx * dx + dy * dy, self.min_r2)
        if r2 > self.cutoff * self.cutoff:
            return # out of force range
        r = sqrt(r2)

        # Very simple short range repulsive force
        coef = (1 - self.cutoff / r) / r2 / self.mass
        self.ax += coef * dx
        self.ay += coef * dy

    def move(self):
        """Move a particle for one timestep. Slightly simplified Velocity Verlet
        integration conserves energy better than explicit Euler method."""
        self.oldx, self.oldy = self.x, self.y

        self.vx += self.ax * self.dt
        self.vy += self.ay * self.dt
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt

        # Bounce from walls
        size = self.box_size
        while self.x < 0 or self.x > size:
            self.x = -self.x if self.x < 0 else 2 * size - self.x
            self.vx = -self.vx
        while self.y < 0 or self.y > size:
            self.y = -self.y if self.y < 0 else 2 * size - self.y
            self.vy = -self.vy

    def move_graphic(self):
        """Move the assoicated graphic of this particle to its new location."""
        if self.graphic:
            dx, dy = self.x - self.oldx, self.y - self.oldy
            self.graphic.move(dx * self.scale_pos, dy * self.scale_pos)

    def move_to(self, x, y):
        """Move particle and graphic directly to the given position."""
        self.oldx, self.oldy = self.x, self.y
        self.x, self.y = x, y
        self.move_graphic()

    @property
    def energy(self):
        """Return the kinetic energy of this particle."""
        return 0.5 * self.mass * (self.vx ** 2 + self.vy ** 2)

    def __repr__(self):
        fmt = "Particle({0}, {1}, {2}, {3}, {4}, {5})"
        return fmt.format(self.x, self.y, self.vx, self.vy, self.ax, self.ay)

    def __getstate__(self):
        """Remove graphic from state that is transferred to another process."""
        state = self.__dict__.copy()
        state['graphic'] = None
        return state

        
##################
# Initialization #
##################

def make_particles(n):
    """Construct a list of n particles in two dimensions, initially distributed
    evenly but with random velocities. The resulting list is not spatially
    sorted."""
    seed(1000)
    sx = ceil(sqrt(n))
    sy = (n + sx - 1) // sx
    start_id = Particle.next_id
    Particle.box_size = sqrt(Particle.density * n)
    particles = [Particle(0, 0, 0, 0, 0, 0) for _ in range(n)]
    size = Particle.box_size

    # Make sure particles are not spatially sorted
    shuffle(particles)

    for p in particles:
        # Distribute particles evenly to ensure proper spacing
        i = p.id - start_id
        p.x = size * (1 + i % sx) / (1 + sx)
        p.y = size * (1 + i / sx) / (1 + sy)

        # Assign random velocities within a bound
        p.vx = random() * 2 - 1
        p.vy = random() * 2 - 1

    return particles

def divide_items(particles, threads, exact=False):
    """Divide the given items among threads threads or processes. If exact,
    threads must evenly divide the number of items. Returns a list of particle
    lists for each thread.

    >>> divide_items([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> divide_items([1, 2, 3, 4, 5, 6, 7, 8], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8]]
    """
    num = len(particles) // threads
    rem = len(particles) % threads
    if exact and rem:
        raise ValueError("threads don't evenly divide particles")

    divided = []
    for i in range(threads):
        start = num * i + (i if i < rem else rem)
        end = start + num + (1 if i < rem else 0)
        divided.append(particles[start:end])

    return divided

def init_graphics(distribution, total, update_interval=1, size=600):
    """Initialize the visualization, if update_interval is nonzero. distribution
    is the set of particles, divided into lists for each thread or process.
    total is the total number of particles. size is the base size of the
    simulation; the window size will be slightly larger."""
    if not update_interval:
        return None, None

    psize = ceil(sqrt(10000 / total)) # particle size
    # Adjust window size so that particle edges do not go off the screen
    wsize = size + psize * 2 + 5
    win = graphics.GraphWin('Particle Simulation', wsize, wsize,
                            autoflush=False)
    win.setBackground('white')

    # Initialize particle graphics
    Particle.scale_pos = size / Particle.box_size
    energy = 0
    for t in range(len(distribution)):
        particles = distribution[t]
        for p in particles:
            p.init_graphic(win, psize, t)
            energy += p.energy

    # Initialize step number
    text = graphics.Text(graphics.Point(wsize // 2, 20),
                         'step = 0, energy = ' + str(energy))
    text.setSize(18)
    text.draw(win)

    return win, text

def update_step(win, text, step, energy, update_interval):
    """Update the visualization if appropriate given the step number and update
    interval."""
    if update_interval and step % update_interval == 0:
        format_str = 'step = {0}, energy = {1}'
        text.setText(format_str.format(step, round(1000 * energy)))
        win.update()

#####################
# Serial Simulation #
#####################

def serial_simulation(n, steps, num_threads=1, normalize_energy=False,
                      update_interval=1):
    """Simulate n particles sequentially for steps steps. num_threads should
    always be 1. update_interval is the visualization update interval."""
    assert num_threads == 1, 'serial_simulation cannot use multiple threads'

    # Create particles
    particles = make_particles(n)
    initial_energy = reduce(lambda x, p: x + p.energy, particles, 0)

    # Initialize visualization
    win, text = init_graphics((particles,), n, update_interval)

    # Perform simulation
    start = time()
    for step in range(steps):
        # Compute forces
        for p1 in particles:
            p1.ax = p1.ay = 0 # reset accleration to 0
            for p2 in particles:
                p1.apply_force(p2)

        # Move particles
        for p in particles:
            p.move()
            # Energy normalization
            p.vx *= Particle.energy_correction
            p.vy *= Particle.energy_correction

        # Update visualization
        energy = 0
        for p in particles:
            p.move_graphic()
            energy += p.energy
        update_step(win, text, step, energy, update_interval)

        # Energy normalization
        if normalize_energy:
            Particle.energy_correction = sqrt(initial_energy / energy)
    end = time()

    print('serial simulation took {0} seconds'.format(end - start))

############################
# Multithreaded Simulation #
############################

def thread_simulation(n, steps, num_threads=4, normalize_energy=False,
                      update_interval=1):
    """Simulate n particles using num_threads threads for steps steps.
    update_interval is the visualization update interval.

    This algorithm uses a barrier to separate the phases that read the
    particles' positions from the phases that write to those positions."""
    # Create particles
    particles = make_particles(n)
    distribution = divide_items(particles, num_threads)
    initial_energy = reduce(lambda x, p: x + p.energy, particles, 0)

    # Create computation threads and barrier
    barrier = threading.Barrier(num_threads + 1)
    threads = [threading.Thread(target=thread_simulate,
                                args=(particles, distribution[i], barrier,
                                      steps, normalize_energy))
               for i in range(num_threads)]

    # Initialize visualization
    win, text = init_graphics(distribution, n, update_interval)

    # Start simulation
    start = time()
    for t in threads:
        t.start() # launch computation threads

    # Handle visualization
    for step in range(steps):
        # Wait for all forces to be computed
        barrier.wait()

        # Wait for all particles to move
        barrier.wait()

        # Update visualization
        energy = 0
        for p in particles:
            p.move_graphic()
            energy += p.energy
        update_step(win, text, step, energy, update_interval)

        # Energy normalization
        if normalize_energy:
            Particle.energy_correction = sqrt(initial_energy / energy)
    end = time()

    print('multithreaded simulation took {0} seconds'.format(end - start))

def thread_simulate(particles, my_particles, barrier, steps, normalize_energy):
    """Perform one thread's part of the simulation for steps steps. particles
    contains all particles in the simulation, my_particles contains just the
    thread's particles, and barrier is the barrier to use for
    synchronization."""
    for step in range(steps):
        # Compute forces on my particles
        for p1 in my_particles:
            p1.ax = p1.ay = 0 # reset accleration to 0
            for p2 in particles:
                p1.apply_force(p2)

        # Wait for all forces to be computed
        barrier.wait()

        # Move my particles
        for p in my_particles:
            p.move()
            # Energy normalization
            p.vx *= Particle.energy_correction
            p.vy *= Particle.energy_correction

        # Wait for all particles to move
        barrier.wait()

###########################
# Multiprocess Simulation #
###########################

def process_simulation(n, steps, num_threads=4, normalize_energy=False,
                       update_interval=1):
    """Simulate n particles using num_threads processes for steps steps.
    update_interval is the visualization update interval.

    This algorithm sets up a circular message passing pipeline between the
    computation processes. In each step, a process injects its particles'
    positions into the pipeline. A process interacts its particles with the
    positions in its own pipeline stage before sending those positions on to the
    next stage. Data in the pipeline completes an entire rotation in each
    step.

    Processes also send their particles' positions to the master in each step in
    order to update the visualization."""
    # Create particles
    particles = make_particles(n)
    distribution = divide_items(particles, num_threads)
    initial_energy = reduce(lambda x, p: x + p.energy, particles, 0)

    # Create processes and message-passing pipes
    master_pipes = [multiprocessing.Pipe() for _ in range(num_threads)]
    p2p_pipes = [multiprocessing.Pipe(False) for _ in range(num_threads)]
    processes = [multiprocessing.Process(target=process_simulate,
                                         args=(distribution[i],
                                               num_threads,
                                               master_pipes[i][1],
                                               p2p_pipes[i][1],
                                               p2p_pipes[(i+1) % num_threads][0],
                                               steps,
                                               Particle.dt, Particle.box_size,
                                               normalize_energy))
               for i in range(num_threads)]
    in_pipes = [pipe[0] for pipe in master_pipes]

    # Initialize visualization
    win, text = init_graphics(distribution, n, update_interval)

    # Start simulation
    start = time()
    for p in processes:
        p.start() # launch computation processes

    for step in range(steps):
        energy = 0
        for t in range(num_threads):
            # Read particle positions from each process
            x_coords, y_coords, partial_energy = in_pipes[t].recv()
            energy += partial_energy

            # Move local particle copies to the appropriate positions
            curr_particles = distribution[t]
            for i in range(len(x_coords)):
                curr_particles[i].move_to(x_coords[i], y_coords[i])
        
        # Update visualization
        update_step(win, text, step, energy, update_interval)

        # Energy normalization
        if normalize_energy:
            ratio = sqrt(initial_energy / energy)
            for t in range(num_threads):
                in_pipes[t].send(ratio)
    end = time()

    print('multiprocess simulation took {0} seconds'.format(end - start))

def process_simulate(my_particles, num_threads, master, left, right, steps,
                     dt, box_size, normalize_energy):
    """Perform one process's part of the simulation for steps steps.
    my_particles contains just the process's particles. num_threads is the total
    number of computation processes. master is a pipe to send data to the master
    process, left is a pipe to send data to the process on the left, and right
    is a pipe to send data to the process on the right. dt is the length of the
    timestep, and box_size is the size of the box."""
    # Set local attributes to match global
    Particle.dt = dt
    Particle.box_size = box_size

    for step in range(steps + 1):
        x_coords, y_coords = [], []
        energy = 0
        for p in my_particles:
            # Copy my particle coordinates to my pipeline stage
            x_coords.append(p.x)
            y_coords.append(p.y)
            energy += p.energy

            # Reset acceleration to 0
            p.ax = p.ay = 0

        # Send coordinates to master
        if step != 0: # no need to send in first step
            master.send((x_coords, y_coords, energy))
        if step == steps:
            return # last step only sends to master

        # Process data for each pipeline rotation
        for t in range(num_threads):
            # Initiate rotation in all but last iteration
            if t != num_threads - 1:
                left.send((x_coords, y_coords))

            # Apply forces from coordinates currently in this pipeline stage
            for p in my_particles:
                for i in range(len(x_coords)):
                    p.apply_force_from_coords(x_coords[i], y_coords[i])

            # Complete rotation in all but last iteration
            if t != num_threads - 1:
                x_coords, y_coords = right.recv()

        # Energy normalization
        if step != 0 and normalize_energy:
            Particle.energy_correction = master.recv()

        # Move my particles for this step
        for p in my_particles:
            p.move()
            # Energy normalization
            p.vx *= Particle.energy_correction
            p.vy *= Particle.energy_correction

##########################
# Command Line Interface #
##########################

@main
def run(*args):
    simulation, num_threads = serial_simulation, 1
    num_particles, steps = default_num_particles, default_steps
    normalize_energy = False
    update_interval = 0
    i = 0
    while i < len(args):
        if args[i] == '-t':
            simulation = thread_simulation
            num_threads = int(args[i+1])
        elif args[i] == '-p':
            simulation = process_simulation
            num_threads = int(args[i+1])
        elif args[i] == '-n':
            num_particles = int(args[i+1])
        elif args[i] == '-s':
            steps = int(args[i+1])
        elif args[i] == '-g' or args[i] == '-v':
            update_interval = 1
            i -= 1
        elif args[i] == '-u':
            update_interval = int(args[i+1])
        elif args[i] == '-dt':
            Particle.dt = float(args[i+1])
        elif args[i] == '-e':
            normalize_energy = True
            i -= 1
        else:
            if args[i] != '-h' and args[i] != '-help':
                print('unknown argument:', args[i], file=sys.stderr)
            print('Options:\n' +
                  '  -t <num>     run with <num> threads\n' +
                  '  -p <num>     run with <num> processes\n' +
                  '  -n <num>     simulate <num> particles\n' +
                  '  -s <num>     run for <num> timesteps\n' +
                  '  -v, -g       enable visualization\n' +
                  '  -u <num>     update visualization every <num> steps\n' +
                  '  -dt <num>    use <num> as length of timestep\n',
                  '  -e           normalize total energy in each timestep',
                  file=sys.stderr)
            return
        i += 2
    simulation(num_particles, steps, num_threads, normalize_energy, update_interval)
