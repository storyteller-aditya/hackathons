# Given an array of integers nums, return a transformed version where each
# element is the product of all elements in the array but the current one
# Example: With nums = [1, 2, 3, 4, 5], the array to be returned is
# [2*3*4*5, 1*3*4*5, 1*2*4*5, 1*2*3*5, 1*2*3*4] i.e. [120, 60, 40, 30, 24]
# Additional Challenge: Try not to use division

# Approach #1:
# Multiply all elements of the array to get the overall product. Then create
# the new array by dividing the overall product by each element of nums.
# Furthermore, to handle the edge case of some elements being zero, while
# building the overall product we do not multiply it any zero we encounter
# and keep a count of the number of zeroes that exist in the array
# If there is more than one zero, we return an array of zeros
# If there is one zero, we set all non-zero places in the transformed
# array to 0 and all zero places to the overall product.
# Time Complexity: O(N) and Space Complexity: O(N)

# Approach #2:
# To adhere to the restriction of the additional challenge, we
# build a binary tree in the following fashion:
# - Each of the numbers in the array is a leaf node
# - Each internal node is formed by multiplying its two children
# The root of the tree contains the product of the entire array,
# its two children contain the product of two halves of the array
# and subsequent children contain the products of increasingly smaller
# partitions of the array.
# Then, for each element in the array we trace its path from leaf to root
# We define the complement child of a node along this path to be the one
# that is not on the path.
# It can be proven that the complement children of all nodes along this path
# contain the products of all non-overlapping partitions that together
# make up the entire array minus the element under consideration.
# Therefore, multiplying the complement children along the path will give
# the product of all elements in the array minus the current one.
# Time Complexity: O(NlogN) and Space Complexity: O(NlogN)

# We implement the approach that adheres to the constraint of the
# additional challenge

from components import Solver


test_cases = [
	{
		"input": {
			"nums": [1, 2, 3, 4, 5]
		},
		"output": [120, 60, 40, 30, 24]
	},
	{
		"input": {
			"nums": [0, 1, 2, 3]
		},
		"output": [6, 0, 0, 0]
	}
]


# The Tree Node containing pointers to left and right children as well as
# its parent, allowing it to built from leaf to root
class Node:
	def __init__(self, left=None, right=None, val=None):
		self.left = left
		self.right = right
		self.parent = None
		if val is not None:
			self.val = val
		else:
			self.val = (left.val if left else 1) * (right.val if right else 1)


def build_tree(array: list[int]) -> list[Node]:
	"""
	Builds the tree from the array in a bottom-up fashion
	:param array: The input array to be converted into a tree
	:return: A list of Nodes
	"""
	leaf_node_array = [Node(val=val) for val in array]
	node_array = [node for node in leaf_node_array]
	# The iterator node_array contains the nodes at a given level of the tree
	# We build the tree level by level till we hit the root level with one node
	while len(node_array) > 1:
		new_node_array = []
		# While building the level we iterate in steps of two, using a node
		# and its neighbor (if it exists) to build its parent node
		for idx in range(0, len(node_array), 2):

			left_node = node_array[idx]
			right_node = node_array[idx+1] if idx+1 < len(node_array) else None
			parent_node = Node(left_node, right_node)

			left_node.parent = parent_node
			if right_node is not None:
				right_node.parent = parent_node
			
			new_node_array.append(parent_node)

		node_array = new_node_array
	return leaf_node_array


def get_product_complement_children(node: Node) -> int:
	"""
	Returns the product of the complement children (as defined in the approach)
	along the path from leaf to root for the given node
	:param node: The leaf Node to start from
	:return: The product of the complement children along the path
	"""
	complement_product = 1
	iterator = node
	while iterator.parent is not None:
		# If the iterator is its parent's left child, then the complement child
		# is the right one, and vice versa
		if iterator.parent.left == iterator:
			complement_child = iterator.parent.right
		else:
			complement_child = iterator.parent.left
		# But this does not guarantee that the complement child does indeed
		# exist, and therefore we check whether it is not None
		if complement_child is not None:
			complement_product *= complement_child.val
		iterator = iterator.parent
	return complement_product 


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		leaf_node_array = build_tree(input_value["nums"])
		transformed_array = [get_product_complement_children(node) 
							 for node in leaf_node_array]
		return transformed_array
