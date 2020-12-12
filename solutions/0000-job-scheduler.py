"""
Problem: 
Implement a job scheduler such that it executes given function f
after a delay of a given n milliseconds
"""

"""
Approach:
We use threading to implement a non-blocking job scheduler
TODO: WRITE APPROACH AND CLEAN CODE
"""


import collections
import heapq
import threading
import time

from components import Solver


func_args = collections.namedtuple("func_args", ["f", "args", "kwargs"])


class JobScheduler:
	def __init__(self):
		# A heapq data structure to track function delays
		# Each element being a tuple of kind (delay, func_args)
		self.func_delays = []
		# Creating a thread to poll for delayed functions to be executed
		self.poll_thread = None
		# A threading condition to indefinitely suspend a thread
		# if the scheduler is running and there are no functions 
		# to be delayed
		self.poll_sleep_condition = threading.Condition()
		# A threading condition to stop a thread
		self.poll_stop_condition = threading.Condition()
		# Creating a flag to as to  whether the scheduler has begun
		self.started = False
		# Creating a flag as to whether the scheduler is accepting jobs
		self.open = True

	def poll(self):
		# The poller function that executes functions with delay
		# It begins by acquiring the lock
		self.poll_sleep_condition.acquire()
		print("Poller has acquired lock")
		while True:
			# If there are no functions, put the poller to sleep
			# to be woken by the later on
			if len(self.func_delays) == 0:
				print("Putting poller to sleep")
				self.poll_sleep_condition.wait()
			# In order to stop the poll thread, we attempt to acquire
			# the poll_stop_condition which is acquired in self.start and can
			# only be released by self.stop()
			if self.poll_stop_condition.acquire(blocking=False):
				print("Breaking the poll thread")
				self.poll_stop_condition.release()
				break
			# If there are functions, pop the earliest one
			delay, function_args = heapq.heappop(self.func_delays)
			sleep_time = max(0, delay - time.time() * 1000) / 1000
			print(f"Sleeping for {sleep_time} seconds")
			time.sleep(sleep_time)
			function_args.f(*function_args.args, **function_args.kwargs)

	def delay(self, f, n, *args, **kwargs):
		if self.open:
			# Adding the function to be executed with some delay
			heapq.heappush(
				self.func_delays,
				(
					time.time() * 1000 + n, 
					func_args(f, args=args, kwargs=kwargs)
				)
			)
			# Checking to see if the poller needs to be woken up
			if (self.started and 
					self.poll_sleep_condition.acquire(blocking=False)):
				print("Waking up poller")
				self.poll_sleep_condition.notify()
				self.poll_sleep_condition.release()
		else:
			print(
				"JobScheduler is now closed and not "
				"accepting any more functions"
			)

	def start(self):
		# Acquires the poll stopping connection
		self.poll_stop_condition.acquire()
		# Creating the thread
		if self.poll_thread is not None:
			print("Thread already exists")
			return
		self.poll_thread = threading.Thread(target=self.poll)
		# Begins the scheduler by starting the poll thread
		print("Starting poller")
		self.started = True
		self.poll_thread.start()

	def stop(self):
		# End the scheduler by stopping the poll thread
		self.open=False
		# While pool is awake, wait by making a blocking call to
		# acquire the underlying lock. It will only be released
		# once all functions have been executed
		print("Waiting for poller")
		self.poll_sleep_condition.acquire()
		# Releases the poll stopping connection and wakes the poll() thread
		# which causes poll() to break its infinite while loop
		self.poll_stop_condition.release()
		self.poll_sleep_condition.notify()
		self.poll_sleep_condition.release()
		self.poll_thread.join()
		self.poll_thread = None
		print("Poller stopped")
		self.started = False

	def reopen(self):
		# Opens the scheduler once more
		self.open = True


results = []
def useful_function(a: int, b: int):
	results.append(a ** b)

scheduler = JobScheduler()
scheduler.delay(useful_function, 1005, a=22, b=3)
scheduler.delay(useful_function, 2015, a=17, b=2)
scheduler.start()
scheduler.stop()
scheduler.delay(useful_function, 2015, a=77, b=2)
scheduler.reopen()
scheduler.delay(useful_function, 15, a=80, b=2)
scheduler.start()
time.sleep(5)
scheduler.delay(useful_function, 15, a=85, b=2)
scheduler.stop()

test_cases = [
	{
		"input": {
			"result": results
		},
		"output": [10648, 289, 6400, 7225]
	}
]


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		return input_value["result"]
