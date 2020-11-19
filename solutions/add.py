# Solves the problem of adding two values a and b
import sys
sys.path.append(".")
from solution import Solver, CheckSolver


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
	

if __name__ == "__main__":
	CheckSolver.check_solver(test_cases, AddSolver())