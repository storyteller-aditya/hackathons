class CheckSolver:
	"""
	A generic class to validate the solution to a problem statement
	which is inherited by all checker classes
	"""
	def __init__(self):
		pass

	@staticmethod
	def check_solver(test_cases: list, solver):
		"""
		Validates that the solver produces the desired output for
		each input test case
		:param test_cases: A list of the input values and the corresponding
			output values for each test case adhering to the following format
			{
				"input": {A dictionary of input arguments}
				"output": The expected output value
			}
		:param solver: A class that inherits the Solver class and 
			implements the solve method for a given problem statement
		:raises: AssertionError: When a test case fails
		:raises: NotImplementedError: When attempting comparison for an
			unexpected output type
		:return: None
		"""
		for test_case in test_cases:
			input_value = test_case["input"]
			output_value = test_case["output"]
			solution_output = solver.solve(input_value)
			error_message = (
				f"Input Arguments:{input_value}"
				f"\nSolution Output: {solution_output}"
				f"\nOutput Value: {output_value}"
			)
			if (isinstance(output_value, int) or isinstance(output_value, float)
					or isinstance(output_value, bool)):
				assert solution_output == output_value, error_message
			elif isinstance(output_value, list):
				for sol, out in zip(solution_output, output_value):
					assert sol == out, error_message
			else:
				raise NotImplementedError
