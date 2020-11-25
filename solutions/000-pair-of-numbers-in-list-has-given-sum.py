# Given a list of numbers nums and a value sum_val, return whether any
# pair of numbers adds up to k in a single pass
# Example: With nums = [10, 15, 3, 7] and sum_val = 17, return True
# since 10+7=17

from components import Solver

test_cases = [
	{
		"input": {
			"nums": [10, 15, 3, 7], 
			"sum_val": 17
		},
		"output": True
	},
	{
		"input": {
			"nums": [10, 15, 3, 7], 
			"sum_val": 19
		},
		"output": True
	}
]


# 'complement_values' is a set containing the complement of the numbers
# observed so far, with complement defined as (sum_val - number)
# If a number is found within complement_values, then its complement
# has been seen before implying that a pair of numbers does exist
complement_values = set()


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		for num in input_value["nums"]:
			# We check whether complement_values contains the current num -
			# if so, then its complement value has been seen before
			if num in complement_values:
				return True
			# Else update it with another complement value to search for
			complement_values.add(input_value["sum_val"] - num)
		return False
