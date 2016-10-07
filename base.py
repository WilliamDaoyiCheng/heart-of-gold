import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import functools

"""
14/09/16
need to check the consistency with the axis labels.
"""


class Heart:
    def __init__(self, grid_x, grid_y, number_of_steps=None):
        self._animation_fig = plt.figure()
        self._grid = np.zeros((grid_x, grid_y), dtype=np.int8)
        self._heart_end = grid_y
        self._heart_circumference = grid_x
        self._animation_data = []
        self._animation_figure = None
        self._im = plt.imshow(self._grid, cmap="gray", interpolation='none', vmin=0, vmax=10)
        self._iterationText = self._animation_fig.text(0, 0, "Time Step: 1")
        self._timeStep = 1
        self._frames = number_of_steps

    def reset(self):
        self._grid = np.zeros((self._heart_circumference, self._heart_end), dtype=np.int8)

    def get_heart(self):
        return self._grid

    def get_heart_end(self):
        return self._heart_end

    def get_heart_circumference(self):
        return self._heart_circumference

    def pulse(self):
        self._grid[:, 0] = 10

    def excite(self, x, y):
        self._grid[x, y] = 10

    def ablate(self, a, b, r):
        y, x = np.ogrid[-a:self._heart_circumference - a, -b:self._heart_end - b]
        mask = x * x + y * y <= r * r

        self._grid[mask] = 20

    def get_time_step(self):
        return self._timeStep

    def dot_pulse(self, a, b, r):
        y, x = np.ogrid[-a:self._heart_circumference - a, -b:self._heart_end - b]
        mask = x * x + y * y <= r * r

        self._grid[mask] = 10

    def find_excited_locations(self):
        """
        Uses .T (transpose) which can only be used on an array. Therefore need to use np.asarray()
        """
        return np.asarray(np.where(self._grid == 8)).T

    def find_excited_location_neighbours(self):
        """
        Returns the neighbour elements given the element position.
        """
        heart_cir = self._heart_circumference
        heart_end = self._heart_end
        excited_cell_list = []

        for excited_location in Heart.find_excited_locations(self):
            x = excited_location[0]
            y = excited_location[1]
            excited_cell_list.append([(x2, y2) for x2 in range(x - 1, x + 2) for y2 in range(y - 1, y + 2) if (
                -1 < x <= heart_cir and -1 < y <= heart_end and (x != x2 or y != y2) and (0 <= x2 < heart_cir) and
                (0 <= y2 < heart_end))])
            # Gives the brick pattern
            excited_cell_list.append(
                [(x, y2) for y2 in [y - 2, y + 2] if (-1 < x <= heart_cir and -1 < y <= heart_end and (y != y2) and
                                                      (0 <= y2 < heart_end))])
        # flattens and removes duplicates.
        return list(set([item for sublist in excited_cell_list for item in sublist]))

    def get_animation_data(self):
        return self._animation_data

    def del_animation_data(self):
        del self._animation_data[:]

    def propagate(self):

        self._timeStep += 1
        self._grid[(self._grid > 0) & (self._grid <= 10)] -= 2

        for potentialSite in Heart.find_excited_location_neighbours(self):

            if self._grid[potentialSite[0], potentialSite[1]] == 0:
                self._grid[potentialSite[0], potentialSite[1]] = 10

    def iterate(self, number_of_steps, pulse_repeat_condition=True, pulse_freq=10):

        interval = 0
        self._frames = number_of_steps
        self._animation_data.append(self._grid.copy())

        for _ in np.arange(number_of_steps):

            interval += 1
            Heart.propagate(self)
            if interval % pulse_freq == 0 and pulse_repeat_condition:
                Heart.pulse(self)
            current_state = self._grid.copy()
            self._animation_data.append(current_state)

    def init(self):

        self._im.set_array(np.zeros((self._heart_circumference, self._heart_end), dtype=np.int8))
        return self._im,

    def animate(self, t):

        self._im.set_array(self._animation_data[t])
        self._iterationText.set_text("Time Step: {0}".format(t + 1))
        return self._im,

    def show_animation(self):

        _ = animation.FuncAnimation(self._animation_fig, functools.partial(Heart.animate, self),
                                    init_func=functools.partial(Heart.init, self), frames=self._frames, interval=1,
                                    repeat=False)
        plt.show()

    def save_animation(self, name_of_file):

        ani = animation.FuncAnimation(self._animation_fig, functools.partial(Heart.animate, self),
                                      init_func=functools.partial(Heart.init, self), frames=self._frames, interval=1,
                                      repeat=False)
        file_name = '%s.mp4' % name_of_file
        ani.save(str(file_name), fps=30, extra_args=['-vcodec', 'libx264'])

    def show_heart(self):
        plt.imshow(Heart.get_heart(self), cmap="gray", interpolation='nearest', vmin=0, vmax=10, origin='lower')
        plt.annotate("Time Step: %s" % (Heart.get_time_step(self)), xy=(1, 0), xycoords='axes fraction', fontsize=16,
                     xytext=(100, -20), textcoords='offset points', ha='right', va='top')
        c_bar = plt.colorbar()
        c_bar.ax.tick_params(labelsize=14)
        c_bar.set_label(r'$S(I,J)}$', fontsize=16, rotation=0, labelpad=25)
        plt.xlabel(r'$J$', fontsize=16, labelpad=12)
        plt.ylabel(r'$I$', fontsize=16, rotation=0, labelpad=15)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()


"""
Get a rotor when used:
a = base.Heart(100,200)
a.exciteCell(50,0)
a.iterate(200,True,40)
"""
