import argparse
import errno
import importlib
import logging
import os

from components import CheckSolver

SOLUTIONS_DIR = os.environ["SOLUTIONS_DIR"]
ATTRIBUTES = ["test_cases", "ProblemSolver"]


def _get_file_and_module_name(problem):
	problem_name = problem.replace(".py", "")
	file_name = f"{SOLUTIONS_DIR}/{problem_name}.py"
	module_name = f"{os.path.basename(SOLUTIONS_DIR)}.{problem_name}"
	return file_name, module_name


def lint_solution(problem):
	file_name, module_name = _get_file_and_module_name(problem)
	if not os.path.isfile(file_name):
		raise FileNotFoundError(
			errno.ENOENT, os.strerror(errno.ENOENT), file_name
		)
	module = importlib.import_module(module_name)
	for attribute in ATTRIBUTES:
		error_message = f"{module_name} does not have {attribute}"
		assert hasattr(module, attribute), error_message


def check_solution(problem):
	_, module_name = _get_file_and_module_name(problem)
	module = importlib.import_module(module_name)
	test_cases = module.test_cases
	solver = module.ProblemSolver
	CheckSolver.check_solver(test_cases, solver())


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--problem", required=False, default="",
						help="Problem statement to validate")
	args = parser.parse_args()
	if args.problem:
		lint_solution(args.problem)
		check_solution(args.problem)

