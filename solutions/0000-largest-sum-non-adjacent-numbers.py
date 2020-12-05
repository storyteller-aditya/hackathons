# Given a list of integers, write a function that returns the largest
# sum of non-adjacent numbers in linear time and constant space.
# Example: 
# [2, 4, 6, 2, 5] should return 13, since we pick 2 + 6 + 5
# [5, 1, 1, 5] should return 10, since we pick 5 + 5

# Approach: Let S(k) be the maximum sum for the array up to idx k.
# Since we cannot select adjacent numbers, the maximum sum possible
# till index k+2 is equal to the larger of three possible sums:
# - The maximum sum till index k plus the element at array[k+2]
# - The maximum sum till index k+1
# - The maximum sum till index k
# The reason behind the first two is that if we pick the element at
# array[k+2] then we can no longer pick up array[k+1] and vice versa.
# The third one is motivated by the fact that negative numbers are
# possible and it might be better to not pick the in-between elements
# at all.
# This can be written down mathematically as:
# S(k+2) = max(S(k) + array[k+2], S(k+1), S(k))
# In order to implement this approach we keep three variables,
# S(k), S(k+1) and S(k+2), and iterate through the array
# using the above to compute the maximum sum upto the iterator idx.
# Time Complexity: O(N) and Space Complexity: O(1)

from components import Solver


test_cases = [
	{
		"input": {
			"array": [2, 4, 6, 2, 5]
		},
		"output": 13
	},
	{
		"input": {
			"array": [5, 1, 1, 5]
		},
		"output": 10
	},
	{
		"input": {
			"array": [5, 1, -1, -5, 10]
		},
		"output": 15
	}
]


def maximum_non_adjacent_sum(array: list[int]) -> int:
	"""
	Computes the maximum sum of non adjacent numbers from the given
	array using the above mentioned approach
	:param array: The array to be processed
	:return: The maximum non adjacent sum
	"""
	length = len(array)
	# The maximum sum for an array with one element is the element itself
	assert length > 1
	if length == 1:
		return array[0]
	sum_k = array[0]

	# With two elements, the maximum sum is the larger of the two elements
	if length == 2:
		return max(array[0], array[1])
	sum_k_plus_1 = max(array[0], array[1])

	for idx in range(2, length):
		# Compute the sum as per the above formula
		sum_k_plus_2 = max(sum_k + array[idx], sum_k_plus_1, sum_k)
		# Reassign the sum variables ahead of the next value of k
		sum_k = sum_k_plus_1
		sum_k_plus_1 = sum_k_plus_2

	return sum_k_plus_2


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
			return maximum_non_adjacent_sum(input_value["array"])
