# https://leetcode.com/problems/time-needed-to-inform-all-employees/
import collections

from components import Solver


test_cases = [
	{
		"input": {"n": 1, "headID": 0, "manager": [-1], "informTime": [0]},
		"output": 0
	},
	{
		"input": {
			"n": 6, "headID": 2, "manager": [2,2,-1,2,2,2],
			"informTime": [0,0,1,0,0,0]
		},
		"output": 1
	},
	{
		"input": {
			"n": 7, "headID": 6, "manager": [1,2,3,4,5,6,-1],
			"informTime": [0,6,5,4,3,2,1]
		},
		"output": 21
	},
	{
		"input": {
			"n": 15, "headID": 0, "manager": [-1,0,0,1,1,2,2,3,3,4,4,5,5,6,6],
			"informTime": [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
		},
		"output": 3
	},
	{
		"input": {
			"n": 4, "headID": 2, "manager": [3,3,-1,2],
			"informTime": [0,0,162,914]
		},
		"output": 1076
	}
]


def get_inform_time(reportee):
	global EMP_CACHE, MANAGER_LIST, INFORM_TIME
	if reportee in EMP_CACHE:
		return EMP_CACHE[reportee]
	if MANAGER_LIST[reportee] == -1:
		time = INFORM_TIME[reportee]
	else:
		time = INFORM_TIME[reportee] + get_inform_time(MANAGER_LIST[reportee])
	EMP_CACHE[reportee] = time
	return time

		
class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		global EMP_CACHE, MANAGER_LIST, INFORM_TIME
		EMP_CACHE = {}
		MANAGER_LIST = input_value["manager"]
		INFORM_TIME = input_value["informTime"]
		return max(
			[
				get_inform_time(reportee)
				for reportee in range(len(INFORM_TIME))
				if INFORM_TIME[reportee] == 0
			]
		)
