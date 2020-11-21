# Solves the problem of adding two values a and b
from components import Solver, CheckSolver

import unittest


test_cases = [
	{
		"input": {"a": 3, "b": 4},
		"output": 7
	},
	{
		"input": {"a": 5, "b": -6},
		"output": -1
	}
]


class AddSolver(Solver):
	def solve(self, input_value: dict):
		return input_value["a"] + input_value["b"]
	

class TestComponents(unittest.TestCase):
	def test_components(self):
		CheckSolver.check_solver(test_cases, AddSolver())