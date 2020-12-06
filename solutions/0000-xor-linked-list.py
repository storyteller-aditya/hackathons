# A XOR linked list is a more memory-efficent way of implementing a
# doubly-ended linked list. A normal doubly-ended linked list contains
# addresses of both its previous element and its next element but a XOR
# linked list contains only the XOR of previous and the next element.
# Implement the add(element) which adds an element to the end and the 
# get(idx) function that returns the element at idx.

# Approach: XOR is a binary mathematical operation that is defined as:
# 0 XOR 0 = 0
# 0 XOR 1 = 1
# 1 XOR 0 = 1
# 1 XOR 1 = 1
# where all numbers are defined in binary (base 2).
# Furthermore, a XOR b is equal to the XOR of the bits comprising a and b
# at the corresponding places.
# We shall use the following pieces in information to solve this problem:
# - a XOR a = 0. This is because when each bit comprising a is XORed
#   with itself the output is 0. 
# - a XOR 0 = a. This is because when each bit comprising a is XORed with 0
#   it returns the value of the bit itself.
# - The XOR operator is associative i.e. (a XOR b) XOR c = a XOR (b XOR c)
# Given three nodes in order X, Y and Z, we compute the address of Z as follows:
# Let address of X be x and the address of Z that we need to compute be z
# Let the XOR of the neigbor addresses of Y be n_y
# Since n_y = x XOR z
# Therefore x XOR n_y = x XOR (x XOR z) = (x XOR x) XOR z = 0 XOR z = z
# Put simply, if we XOR the address of the previous element with the
# XOR of neighbors of the current element we get the address of the next.
# This is how we implement the get(idx) operation in O(N).
# Further, add(element) is merely creating a new node after iterating
# to the end of the list.


from components import Solver


class Node:
	def __init__(self, element: int, address: int) -> None:
		"""
		Initializing the variables needed for a node of the XOR Linked List
		:return: None
		"""
		self.element = element
		self.address = address
		self.both = None

	def __str__(self) -> None:
		"""
		Overriding the method to print the node
		:return: None
		"""
		return (
			f"Element: {self.element} | Address: {self.address} | "
			f"Both: {self.both}"
		)


def get_next_address(previous_address: int, both_addresses_xored: int) -> int:
	"""
	Returns the next address given the previous address and the 
	xor of previous and next addresses
	:param previous_address: The address of the previous node
	:param both_addresses_xored: The XOR of the previous and the next node
	:return: The address of the next node
	"""
	# For the root node, the previous address is None and therefore the next
	# address is stored directly in both_addresses_xored
	if previous_address is None:
		next_address = both_addresses_xored
	# Otherwise we XOR the two as per the above approach
	else:
		next_address = previous_address ^ both_addresses_xored
	return next_address


class XORLinkedList:
	def __init__(self) -> None:
		"""
		Initializing the variables needed for a XOR Linked List
		:return: None
		"""
		# We mimick a pool of addresses as a dictionary
		self.address_pool = {}
		# The root element
		self.root = None

	def add(self, element: int) -> None:
		"""
		Adds an element to the XOR Linked List
		:param element: The element to be added to the list
		:return: None
		"""
		# Handling the case when the list is empty
		if self.root is None:
			node = Node(element=element, address=0)
			self.root = node
			self.address_pool[0] = node # Housekeeping to maintain address pool
			return

		# Iterating to the end of the existing list
		iterator = self.root
		previous_address = None
		while iterator.both is not None:
			next_address = get_next_address(previous_address, iterator.both)
			previous_address = iterator.address
			iterator = self.address_pool[next_address]

		# Create the new node. For simplicity of implementation the address
		# we assign to a new element will be 2 + address of previous element
		node = Node(element=element, address=iterator.address+2)
		# Updating address pool with the newly node created
		self.address_pool[node.address] = node 

		# Modify the last element to hold the XOR of the address
		# of the node before it and the new node to be added
		if previous_address is None:
			iterator.both = node.address
		else:
			iterator.both = previous_address ^ node.address

	def get(self, index: int) -> int:
		"""
		Obtains the element at a given index
		:param index: The index for which the element is to be returned
		:return: The element at the index
		"""
		idx = 0
		iterator = self.root
		previous_address = None
		# Iterate over the list, ending when the index is reached or the
		# end of the list is
		while idx < index and iterator.both is not None:
			idx += 1
			next_address = get_next_address(previous_address, iterator.both)
			previous_address = iterator.address
			iterator = self.address_pool[next_address]
		# If the index is within the bounds of the list, else -1
		if idx == index:
			return iterator.element
		else:
			return -1

	def __str__(self) -> None:
		"""
		Overriding the method to print the linked list
		:return: None
		"""
		string = []
		iterator = self.root
		previous_address = None
		string.append(str(iterator))
		# Iterate over the list
		while iterator.both is not None:
			next_address = get_next_address(previous_address, iterator.both)
			previous_address = iterator.address
			iterator = self.address_pool[next_address]
			string.append(str(iterator))
		return "\n".join(string)


xor_linked_list = XORLinkedList()
for idx in range(10):
	xor_linked_list.add(12 * idx)
# print(xor_linked_list) # Uncomment to view the linked list

# The test cases create a tree, serialize and deserialize it,
# and test for the value of one of the node
test_cases = [
	{
		"input": {
			"value": xor_linked_list.get(3)
		},
		"output": 36
	},
	{
		"input": {
			"value": xor_linked_list.get(7)
		},
		"output": 84
	},
	{
		"input": {
			"value": xor_linked_list.get(11)
		},
		"output": -1
	}
]


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		return input_value["value"]