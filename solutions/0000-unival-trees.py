"""
Problem:
A unival (universal) tree is one where all nodes have the same value
Given the root of a binary tree, count the number of unival subtrees under it.
"""

"""
Approach: 
Given a root node of a binary tree with value X, the conditions
for it to be considered a unival tree are:
- The left subtree is a unival tree of value X
- The right subtree is a unival tree of value X
As a base case, a leaf node is always a unival tree.
In order to count all unival trees, we keep a global counter
and recursively
Average Time Complexity: O(N)
Why: The time complexity is O(2^Height) because the number of possible
unival trees to check doubles at each level of the tree.
Since the height of a binary is on average O(logN), the average time
complexity is given as O(2^logN) = O(N)
Average Space Complexity: O(logN)
Why: The space complexity is O(Height) because that is the maximum number of
function calls in the stack at any time.
Since the height of a binary is on average O(logN), the average space 
complexity is given as O()
"""


from collections import namedtuple

from components import Solver


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# The tree that is created looks like:
#   0
#  / \
# 1   0
#    / \
#   1   0
#  / \
# 1   1
# It contains a total of 5 unival trees (4 leaves plus 
# one two-level unival tree)
test_cases = [
	{
		"input": {
			"root_node": Node(
						val=0, 
						left=Node(1), 
						right=Node(
							val=0,
							left=Node(
								val=1,
								left=Node(1),
								right=Node(1)
							),
							right=Node(0)
						)
					)
		},
		"output": 5
	}
]


unival_count_ret_val = namedtuple(
	"unival_count_ret_val", ["count", "is_child_unival"]
)


def count_unival_trees(root_node):
	"""
	Returns the number of unival trees for the tree with root root_node
	:param root_node: The root of the tree
	:returns: A namedtuple of type unival_count_ret_val
	"""
	# Handle the base case for a leaf node
	if root_node.left is None and root_node.right is None:
		return unival_count_ret_val(count=1, is_child_unival=True)
	# To keep a count of the unival trees rooted at root_node
	self_count = 0
	# To check if the tree at root_node is itself unival
	self_unival = True
	# Probe the left and right subtree if they exist
	for child in [root_node.left, root_node.right]:
		if child is not None:
			child_unival_count_ret_val = count_unival_trees(child)
			self_count += child_unival_count_ret_val.count
			self_unival = (
				self_unival 
				# For the root_node tree to be unival, its child must be too
				and child_unival_count_ret_val.is_child_unival
				# and the root_node val must match child val
				and root_node.val == child.val
			)
	# If it itself is unival, increment self_count by 1
	if self_unival:
		self_count += 1
	# Return the results from probing root_node
	return unival_count_ret_val(count=self_count, is_child_unival=self_unival)


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		return count_unival_trees(input_value["root_node"]).count