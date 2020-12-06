# Given an array of integers, find the first missing positive 
# integer in linear time and constant space. The array can 
# contain duplicates and negative numbers as well.
# You can modify the input array in-place.
# Example: The array [3, 4, -1, 1] should give 2 and the array
# [1, 2, 0] should give 3.

# Approach:
# We begin by removing negative numbers in-place and then finding
# the minimum of the array. 
# After that we turn the array into a set to reduce the time complexity
# of checking whether a number exists in the input array to O(1).
# Finally, we start with the min_val + 1 and check whether it exists
# in the set. If so, we check for min_value + 2, min_value + 3 and so on
# until we finally arrive at a number that does not exist.
# This number is the first positive hole to be returned.
# The time complexity of this approach is O(N) because we need to perform
# at most as many look ups as elements in an array in the worst case
# scenario which occurs when the array is of the form [1, 2, ..., N]
# i.e. when it has no holes at all.

from components import Solver


test_cases = [
	{
		"input": {
			"array": [3, 4, -1, 1]
		},
		"output": 2
	},
	{
		"input": {
			"array": [1, 2, 0]
		},
		"output": 3
	}
]

def first_missing_positive_integer(array: list[int]) -> int:
	"""
	Returns the first missing positive integer for a given array
	using the above algorithm
	:param array: The input array
	:return: The first missing positive integer
	"""
	# Remove negative numbers and identify the minimum value
	array = [val for val in array if val >= 0]
	min_val = min(array)

	# Turn it into a set in constant memory
	array_set = set()
	while len(array) > 0:
		val = array.pop()
		array_set.add(val)
	
	# Identify the hole by looking up elements starting from
	# the minimum value
	hole = min_val + 1
	while hole in array_set:
		hole += 1

	return hole


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		return first_missing_positive_integer(input_value["array"])