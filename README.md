# Solutions to LeetCode Problems

This repository holds the solutions to various LeetCode problems that I have practiced over time.

## Composition of the Repo
- components: This package defines the classes that make up every solution:
	- An abstract Solver class with its abstract solve() method that every solution implements
	- A CheckSolver class that is used to validate that the solver produces the expected behavior for each of the test_cases passed
- scripts: This directory contains scripts to perform actions such as:
	- Creating a virtual environment
	- Running tests for the components 
	- Validating that the solutions to all problems implemented are indeed correct
- solutions: This directory holds the solutions to all problems encountered so far
- test: The test scripts for various components


## Anatomy of a Solution
- Each solution begins with a comment linking to the appropriate LeetCode problem statement and its description
- Following that, the test cases are defined as a list of dictionaries, each one containing two keys - the "input" and the desired "output"
- Finally, a ProblemSolver class inherits the Solver and defines the solve() method


## How to Validate the Solutions
In order to validate all solutions, execute the following command:
```bash
bash scripts/validate_solutions.sh
```

It will create / activate the virtual environment and then ensure that the TestSolver executes correctly for each of the solutions in the solutions/ directory.

In order to validate the correctness of a given solution, execute the following command instead:
```bash
bash scripts/validate_solutions.sh FILENAME.py
```