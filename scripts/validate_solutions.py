import argparse
import errno
import importlib
import logging
import os
import typing

from components import CheckSolver


logging.basicConfig(
	format='%(asctime)s - %(message)s', 
	datefmt='%d-%b-%y %H:%M:%S', 
	level=logging.INFO
)
LOGGER = logging.getLogger()


SOLUTIONS_DIR = os.environ["SOLUTIONS_DIR"]
ATTRIBUTES = ["test_cases", "ProblemSolver"]


def _get_file_and_module_name(problem: str) -> typing.Tuple[str, str]:
	"""
	Parses the problem passed into the file and the module name which
	are used in linting
	:param problem: The problem to be parsed
	:return: The corresponding file name and the module name to be imported
	"""
	problem_name = problem.replace(".py", "")
	file_name = f"{SOLUTIONS_DIR}/{problem_name}.py"
	module_name = f"{os.path.basename(SOLUTIONS_DIR)}.{problem_name}"
	return file_name, module_name


def _get_all_problems() -> typing.List[str]:
	"""
	Identifies all problems for which solutions exist
	:return: A list of problems found
	"""
	return [
		file_name for file_name in os.listdir(SOLUTIONS_DIR) 
		if file_name.endswith(".py")
	]


def lint_solution(problem: str):
	"""
	Acts as a lint for the given solution, ensuring that it has been written
	in the correct format so as to be checked
	:param problem: The problem to be linted
	:raises: FileNotFoundError: When the solution does not exist
	:raises: AssertionError: When the solution has been improperly written
	:return: None
	"""
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
	"""
	Checks the behavior of the given solution for correctness
	:param problem: The problem to be linted
	:raises: AssertionError: When the solution is incorrect
	:return: None
	"""
	_, module_name = _get_file_and_module_name(problem)
	module = importlib.import_module(module_name)
	test_cases = module.test_cases
	solver = module.ProblemSolver
	CheckSolver.check_solver(test_cases, solver())


def lint(args):
	"""
	Lints all solutions that have been written
	:param args: The arguments passed (No arguments used)
	:raises: FileNotFoundError: When the solution does not exist
	:raises: AssertionError: When the solution has been improperly written
	:return: None
	"""
	for file_name in _get_all_problems():
		LOGGER.info(f"Linting {file_name}")
		lint_solution(file_name)
		LOGGER.info(f"{file_name} is correctly written")


def check(args):
	"""
	Checks solutions that have been written
	:param args: The arguments passed (if args.problem is specified it only
		checks that problem, else it checks asll)
	:raises: AssertionError: When the solution is incorrect
	:return: None
	"""
	if args.problem:
		file_names = [args.problem]
	else:
		file_names = _get_all_problems()

	for file_name in file_names:
		LOGGER.info(f"Checking {file_name}")
		lint_solution(file_name)
		check_solution(file_name)
		LOGGER.info(f"{file_name} is correct")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	# Lint problems
	lint_parser = subparsers.add_parser('lint', help='Lint all problems')
	lint_parser.set_defaults(func=lint)

	# Check problems
	check_parser = subparsers.add_parser('check', help='Check all problems')
	check_parser.add_argument("--problem", required=False, default="",
						      help="Problem statement to check")
	check_parser.set_defaults(func=check)

	args = parser.parse_args()
	args.func(args)
