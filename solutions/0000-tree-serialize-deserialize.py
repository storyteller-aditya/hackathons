"""
Problem:
Given the root of a binary tree, implement functions to serialize()
the tree into a string and deserialize() it back into a tree
"""

"""
Approach: 
In order to convert a tree into a string we proceed with an pre-order
traversal of the tree and create a string of the following format:
Node [Representation for Left SubTree] [Representation for Right SubTree]
with the Representations being generated in a recursive fashion.
Thereafter, in order to deserialize this tree, we define a function
that splits this string into three pieces:
- Node
- Left Sub Tree
- Right Sub Tree
This can be done by finding the Square Bracket that closes the first
opening Square Bracket
In this way we can serialize a tree into a string in O(N) time complexity
and deserialize it with average time complexity O(NlogN) [since the function
to split a string into three pieces is at most O(N), the average height
of a binary tree is of the order of O(logN) and we perform as many splits
as the height to restore the tree].
However, the deserialization is worst-case O(N^2) in degenerate scenarios
such as when each node's right child does not exist. This occurs because
the height of the tree is now O(N) and each split has complexity O(N), and
on combining them we obtain the worst-case time complexity of O(N^2).
To alleviate this worst-case time complexity scenario, we build in a special
trick - we check if the string has an empty pair of brackets near the beginning
or at the end, a signal that one of the children is empty but the other is not.
As a result, the split becomes O(1) and this degenerate case time complexity
now reduces to O(N).
"""


from components import Solver


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def serialize(root_node) -> str:
	"""
	Serializes the tree into a string of the form Node [LeftTree] [RightTree]
	:param root_node: The root of the tree
	:return: A string representing the serialized version of the tree
	"""
	if root_node is None:
		return ""
	elif root_node.left is None and root_node.right is None:
		return f"{root_node.val} [] []"
	else:
		return (
			f"{root_node.val} "
			f"[{serialize(root_node.left)}] "
			f"[{serialize(root_node.right)}]"
		)


def deserialize(serialized: str):
	"""
	Deserializes a serialized tree string back into a tree
	:param serialized: The serialized tree string
	:return: A Node representing the root of the tree
	"""
	# A serialized tree is always of format val [...] [...]
	# and with this we isolate the val from the child trees
	val, child_trees = serialized.split(" ", 1)
	# The child_trees of a leaf node are of the form '[] []'
	if child_trees.endswith("[]") and child_trees.startswith("[]"):
		return Node(val)
	# But if only the right one is empty, child_trees ends with '[]'
	elif child_trees.endswith("[]"):
		left_sub_tree = child_trees[1:-4] # Removes enclosing [] too
		return Node(val, left=deserialize(left_sub_tree))
	# Similarly if only the left one is empty, child_trees starts with '[]'
	elif child_trees.startswith("[]"):
		right_sub_tree = child_trees[3:-1] # Removes enclosing [] too
		return Node(val, left=deserialize(right_sub_tree))
	# But if neither are empty we employ a bracket matching algorithm
	else:
		# By counting '[' and ']', we try to find the idx of the
		# closing bracket of the left sub-tree
		brackets = 0
		for idx in range(len(child_trees)):
			if child_trees[idx] == "[":
				brackets += 1
			elif child_trees[idx] == "]":
				brackets -= 1
			if brackets == 0:
				partition_idx = idx
				break
		left_sub_tree = child_trees[1:partition_idx]
		right_sub_tree = child_trees[partition_idx+3:-1]
		return Node(
			val, left=deserialize(left_sub_tree), 
			right=deserialize(right_sub_tree)
		)


# The test cases create a tree, serialize and deserialize it,
# and test for the value of one of the node
test_cases = [
	{
		"input": {
			"value": deserialize(
				serialize(
					Node(
						"root", 
						Node("left", Node("left.left")), 
						Node("right")
					)
				)
			).left.left.val
		},
		"output": "left.left"
	},
	{
		"input": {
			"value": deserialize(serialize(Node("root"))).val
		},
		"output": "root"
	}
]


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		return input_value["value"]