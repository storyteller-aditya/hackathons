class Solver:
	"""
	A generic class to implement the solution to a problem statement
	which is inherited by all solution classes
	"""
	def __init__(self):
		pass

	def solve(self, input_value: dict):
		"""
		The method which implements the solution to a problem statement
		:param input_value: The input values for a test case, expressed 
			as a dictionary of arguments
		:return: The output value for the corresponding input test case
		"""
		raise NotImplementedError
