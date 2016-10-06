import numpy as np 
from scipy.ndimage import measurements
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import functools

"""
14/09/16
need to check the consistency with the axis labels.
"""

class heart:

	def __init__(self, grid_x, grid_y):
		self._grid = np.zeros((grid_x, grid_y), dtype = np.int8)
		self._heart_end = grid_y
		self._heart_circumference = grid_x
		self._animation_data = []
		self._animation_figure = None
		self._iterationText = None
		self._timeStep = 1

	def reset(self):
		self._grid = np.zeros((self._heart_circumference,self._heart_end), dtype = np.int8)

	def get_heart(self):
		return self._grid

	def get_heart_end(self):
		return self._heart_end

	def get_heart_circumference(self):
		return self._heart_circumference

	def pulse(self):
		self._grid[:,0] = 10

	def tester(self,x,y):
		self._grid[x,y] = 10

	def ablate(self, a, b, r):
		y,x = np.ogrid[-a:self._heart_circumference - a, -b:self._heart_end - b]
		mask = x*x + y*y <= r*r

		self._grid[mask] = 20

	def getTimeStep(self):
		return self._timeStep

	def localPulse(self, a, b, r):
		y,x = np.ogrid[-a:self._heart_circumference - a, -b:self._heart_end - b]
		mask = x*x + y*y <= r*r

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
		X = self._heart_circumference
		Y = self._heart_end
		excitedList = []

		for excited_location in heart.find_excited_locations(self):
			x = excited_location[0]
			y = excited_location[1]
			excitedList.append([(x2, y2) for x2 in range(x-1, x+2) for y2 in range(y-1,y+2) if (-1 < x <= X and -1 < y <= Y and (x != x2 or y != y2) and (0 <= x2 < X) and (0 <= y2 < Y))])
			#Gives the brick pattern
			excitedList.append([(x, y2) for y2 in [y-2, y+2] if (-1 < x <= X and -1 < y <= Y and (y != y2) and (0 <= y2 < Y))])
		# flattens and removes duplicates.
		return list(set([item for sublist in excitedList for item in sublist]))

	def get_animation_data(self):
		return self._animation_data
		print test_data

	def del_animation_data(self):
		del self._animation_data[:]

	#Old method for propogation.
	def propagate_old(self):

		self._grid[(self._grid > 0) & (self._grid <= 10)] -= 2

		for excited_location in heart.find_excited_locations(self):

			#starting pulse sites (column 0)
			if excited_location[1] == 0:

				if self._grid[excited_location[0],excited_location[1] + 1] == 0:
					self._grid[excited_location[0],excited_location[1] + 1] = 10

			#end cell
			if excited_location[1] == self._heart_end - 1:

				pass

			#any cell inbetween the open boundrys
			if excited_location[1] > 0 and excited_location[1] < self._heart_end - 1:

				if self._grid[excited_location[0],excited_location[1] + 1] == 0:
					self._grid[excited_location[0],excited_location[1] + 1] = 10

				if self._grid[excited_location[0],excited_location[1] - 1] == 0:
					self._grid[excited_location[0],excited_location[1] - 1] = 10

	def propagate(self):

		self._timeStep += 1
		self._grid[(self._grid > 0) & (self._grid <= 10)] -= 2

		for potentialSite in heart.find_excited_location_neighbours(self):

			if self._grid[potentialSite[0],potentialSite[1]] == 0:
					self._grid[potentialSite[0],potentialSite[1]] = 10

	def iterate(self, number_of_steps, pulseRepeat = True , pulseFreq = 10):

		interval = 0
		self._frames = number_of_steps
		self._animation_data.append(self._grid.copy())

		for n in np.arange(number_of_steps):

			interval += 1
			heart.propagate(self)
			if interval % pulseFreq == 0 and pulseRepeat == True:
				heart.pulse(self)
			current_state = self._grid.copy()
			self._animation_data.append(current_state)

	def create_anifigure(self):
		self._anifig = plt.figure()
		self._im = plt.imshow(self._grid, cmap = "gray", interpolation='none', vmin = 0, vmax = 10)
		self._iterationText = self._anifig.text(0,0,"Time Step: 1")

	def init(self):

		self._im.set_array(np.zeros((self._heart_circumference, self._heart_end), dtype = np.int8))
		return self._im,

	def animate(self,t):

		self._im.set_array(self._animation_data[t])
		self._iterationText.set_text("Time Step: {0}".format(t+1))
		return self._im,

	def show_animation(self):

		ani = animation.FuncAnimation(self._anifig, functools.partial(heart.animate,self), init_func = functools.partial(heart.init,self), frames = self._frames, interval = 1, repeat = False)
		plt.show()

	def save_animation(self, name_of_file):

		ani = animation.FuncAnimation(self._anifig, functools.partial(heart.animate,self), init_func = functools.partial(heart.init,self), frames = self._frames, interval = 1, repeat = False)
		file_name = '%s.mp4' %name_of_file
		ani.save( str(file_name), fps=30, extra_args=['-vcodec', 'libx264'])

class image():

	def show_heart(self, heart):
		heart_image = plt.imshow(heart.get_heart(), cmap = "gray", interpolation='nearest', vmin = 0, vmax = 10)
		plt.annotate("Time Step: %s" %(heart.getTimeStep()), xy = (1,0), xycoords='axes fraction', fontsize=16, xytext=(100, -20), textcoords='offset points', ha='right', va='top')
		cbar = plt.colorbar()
		cbar.ax.tick_params(labelsize = 14)
		cbar.set_label(r'$S(I,J)}$', fontsize = 16, rotation = 0, labelpad = 25)
		plt.xlabel(r'$J$', fontsize = 16, labelpad = 12)
		plt.ylabel(r'$I$', fontsize = 16, rotation = 0, labelpad = 15)
		plt.xticks(fontsize = 14)
		plt.yticks(fontsize = 14)
		plt.show()

"""
Get a rotor when used:
a = base.heart(100,200)
a.tester(50,0)
a.iterate(200,True,40)
"""