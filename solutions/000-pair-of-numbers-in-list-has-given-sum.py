# Given a list of numbers nums and a value sum_val, return whether any
# pair of numbers adds up to k in a single pass
# Example: With nums = [10, 15, 3, 7] and sum_val = 17, return True
# since 10+7=17

# Approach: 
# We define the complement of a number as (sum_val - number)
# Our solution is to iterate once through nums while performing
# the following two operations:
# - Building a set containing the complement of the numbers observed so far
# - Checking if the current number is found within this set
# If the current number is found within this set, then that implies that its
# complement value has been before in nums. In other words, a pair of numbers
# adding to the sum_val does indeed exist and it is equal to 
# (current number, sum_val - current number)
# Time Complexity: O(N)

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


# 'complement_values' is a set containing the complements of the numbers
# observed so far while iterating through nums
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
