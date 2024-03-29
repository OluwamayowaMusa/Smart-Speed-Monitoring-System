import math
import numpy as np
from collections import defaultdict, deque

class Tracker:
	""" Tracks Objects in a Frame and measures the speed.
	
	Tracker class 
	 -> Tracks objects in a frame and assign a unique Id.
		  @ Operates based on the property midpoint of the top most left 
			and bottom right is also conserved.
	 -> Measures the speed of the object based on two models:
		  @ Model One works based on measuring the traveling time in
		    a given unit of distance
		  @ Model Two works based on measuring the moving distance in
			a given unit of time
		  
	Attributes:
		model_one:  Decides the model to use.
		distance_offset: Diffrence Allowed in Euclidean Distance
		object_info: A Dictionary containing the object_id and info
					 about the objects
		id_: Stores the present id of object
		going_down: A list that stores the object_id of object going down
		gone_down: A list that stores the object_id of object gone down
		object_time_stamp: A list that stores the time stamp of objects 
						   i.e before and after
		coordinates_y: Stores the coordinate of y for an object in every 
					   frame per sec
	"""
	
	def __init__(self, model_one=True, distance_offset=90, fps=3):
		""" Intializes the Tracker Object
		
		Args:
			model_one: Condition to determine the model
			distance_offset: Allowed margin of error in distance
			fps: Number of frames per second
		"""
		self.object_info = {}
		self.distance_offset = distance_offset
		self.id_ = 0
		if model_one:
			self.going_down = []
			self.gone_down = []
			self.object_time_stamp = [0, 0]
		else:
			self.coordinates_y = defaultdict(lambda: deque(maxlen=fps))
			
	def populate_coordinates_y(self, id_, y_coordinate):
		""" Populate the Coordinate y property
		
		Args:
			id_: Object Id
			y_cordinate: Position of the object on the y axis
		"""
		self.coordinates_y[id_].append(y_coordinate)
	
	def calculate_object_speed_in_km_per_hr_model_two(self, id_):
		""" Calculate Speed of the object from measuring the 
			distance in a unit of time
		
		Args:
			id_: Object id
			
		Returns:
			Speed of moving object
		"""
		coordinate_start = self.coordinates_y[id_][0]
		coordinate_end = self.coordinates_y[id_][-1]
		distance_covered = abs(coordinate_end - coordinate_start)
		time = len(self.coordinates_y[id_]) / self.coordinates_y[id_].maxlen
		speed = round(distance_covered / time * 3.6)
		
		return speed
		
	def populate_going_down(self, id_):
		""" Add Id to list of object going down
		
		Args:
			id_: Object_id to be added
		"""
		self.going_down.append(id_)
		
	def populate_object_time_stamp(self, time, before=True):
		""" Populate the object time stamp
		
		Args:
			time: Time Instance
			before: Condition to determin before or after
		"""
		if before:
			self.object_time_stamp[0] = time
		else:
			self.object_time_stamp[1] = time
		
			
	def calculate_object_speed_in_km_per_hr_model_one(self, distance):
		""" Calculate the speed from object time stamp
		
		Args:
			distance: Distance covered by moving vehicle
		
		Returns:
			Speed of object in Km/hr
		"""
		elapsed_time = abs(self.object_time_stamp[1] - self.object_time_stamp[0])
		speed = round(distance/elapsed_time * 3.6)
		
		return speed
		
	def calculate_object_speed_in_metere_per_sec(self, distance):
		""" Calculate the speed from object time stamp
		
		Args:
			distance: Distance covered by moving vehicle
		
		Returns:
			Speed of object in m/s
		"""
		return round(self.calculate_object_speed_in_km_per_hr(distance)/3.6)
		
		
	def populate_gone_down(self, id_):
		""" Add Id to list of object gone down
		
		Remove the obejct id from going down and add object id to gone
		down if object_id is not recent
		
		
		Args:
			id_: Object_id to be added
		"""

		self.going_down.remove(id_)
		
		if len(self.gone_down) == 0:
			self.gone_down.append(id_)
		elif id_ != self.gone_down[-1]:
			self.gone_down.append(id_)
		
		
	def assign_id(self, first_coordinate, second_coordinate):
		""" Assigns Id to objects based on the Coordinate
		
		Args:
			first_coordinate: Top left corner (x1, y1)
			second_coordinate: Bottom right corner (x2, y2)
			
		Returns:
			Object Id
		"""
		mid_point = self.get_object_info(first_coordinate, second_coordinate)
		
		if self.object_has_been_detected_before(mid_point,):
			self.object_info[self.id_] = {"mid_point": mid_point}
			object_id = self.id_
		else:
			object_id = len(self.object_info) + 1
			self.object_info[object_id] = {"mid_point": mid_point}
		
		return object_id
			
	def object_has_been_detected_before(self, mid_point):
		""" Check if the object has been Detected before
		
		Args:
			area: Area enclosed by object
			mid_point: Midpoint of two coordinates
			n_difference: Difference between normalized mid_point
			
		Returns:
			True if detected before, otherwise false
		"""
		if len(self.object_info) == 0:
			return False
			
		for id_, info in self.object_info.items():
			 distance_change = self.calculate_euclidean_distance(mid_point, info["mid_point"])
			 if distance_change < self.distance_offset:
				 self.id_ = id_
				 return True
				 
		return False
		
		
	@classmethod
	def get_object_info(cls, first_coordinate, second_coordinate):
		""" Calculate the properties i.e mid_point of 
			the coordinates peculiar to an object
			
		Normalised Mid-point means the mid_point / Area
		
		Args:
			first_coordinate: (x1, y1)
			second_coordinate: (x2, y2)
			
		Returns:
			mid_point
		"""
		mid_point = cls.calculate_midpoint(first_coordinate, second_coordinate)
		
		return mid_point
		
	@staticmethod
	def calculate_area(length, breadth):
		""" Calculate the Area covered by Object
		
		Args:
			length: Length of bounding box
			breadth: Breadth of bounding box
			
		Returns:
			Area Eneclosed
		"""
		return length * breadth
		
	@staticmethod
	def calculate_midpoint(first_coordinate, second_coordinate):
		""" Calculate the Midpoint of a line
		
		Args:
			first_coordinate: (x1, y1)
			second_coordinate: (x2, y2)
			
		Returns:
			Midpoint of the line
		"""
		
		mid_x = (first_coordinate[0] + second_coordinate[0])/2
		mid_y = (first_coordinate[1] + second_coordinate[1])/2
		
		return np.array((mid_x, mid_y))
		
	@staticmethod	
	def calculate_euclidean_distance(first_coordinate, second_coordinate):
		""" Calculate the Euclidean Distance
		
		Args:
			first_coordinate: (x1, y1)
			second_coordinate: (x2, y2)
			
		Returns:
			Euclidean Distance			
		"""
		x_difference = abs(first_coordinate[0] - second_coordinate[0])
		y_difference = abs(first_coordinate[1] - second_coordinate[1])
		
		return math.hypot(x_difference, y_difference)
