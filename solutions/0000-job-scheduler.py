"""
Problem: 
Implement a job scheduler such that it executes given function f
after a delay of a given n milliseconds
"""

"""
Approach:
We use threading to implement a job scheduler that can execute
an arbitrary number of functions with specified delays from the current time.

The design of this scheduler consists of two threads:
- A main control thread handling the addition of functions to be scheduled
  as well as the starting and stopping of the scheduler thread
- A scheduler thread that evaluate the scheduled functions with the specified
  amount of time

Given the GIL, only one thread can be running at any time and as a result
if we are using threading then we are limited to the execution of a single
delayed function at time. Therefore having the scheduler manage a new thread 
per function being scheduled is a level of complexity that we can avoid
in a vanilla implementation.

In our implementation, we use a heapq to maintain the list of functions
to be executed along with their delay. This ensures that we can identify
the next function to be executed (with minimum delay from the current time)
in O(1) time complexity at the cost of (logN) insertion time complexity.

Furthermore, we use the following constructs to synchronize the behavior:
- A lock which helps facilitate the submission of functions to the scheduler
  in a synchronous fashion. It is held and released alternately by:
  ~ The submission function as it adds to the heapq
  ~ The scheduler thread as it removes from heapq to 
    execute the delayed functions
- A lock which is held by the main thread as long as the scheduler thread
  should continue to run. If the main thread releases the lock then the
  scheduler thread immediately exits.
- A condition which allows us to put the scheduler thread to sleep when
  it runs out of functions to schedule and wake it up again when new functions
  are added or when we want to wake the scheduler to stop it.
"""


import collections
import heapq
import threading
import time

from components import Solver

# Uncomment out all print statements to examine inner workings


class FunctionWithArguments:
	# This class that wraps a function and the args and kwargs 
	# that it should be called with
	def __init__(self, func, *args, **kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs

	def __call__(self):
		# Overridding the class callable method so that the function can be 
		# cleanly invoked with given args and kwargs
		return self.func(*self.args, **self.kwargs)


# A namedtuple to encapsulate a function with arguments to be executed with
# a given amount of delay (in milliseconds) from the current time
delayed_function = collections.namedtuple(
	"delayed_function", 
	["delay", "func_with_args"]
)


class DelayedFunctionsHeap:
	# This class ensures synchronous insertion and removal of
	# delayed functions into the heap
	def __init__(self):
		# A heapq data structure to track function delays with
		# each element being a tuple of kind delayed_function
		self.delayed_functions = []
		# A lock for synchronous behavior
		self.lock = threading.Lock()

	def insert(self, n, func, *args, **kwargs):
		# Inserts an element into the heap synchronously
		self.lock.acquire()
		heapq.heappush(
			self.delayed_functions,
			delayed_function(
				delay=time.time() * 1000 + n, 
				func_with_args=FunctionWithArguments(func, *args, **kwargs)
			)
		)
		self.lock.release()

	def remove(self):
		# Removes an element from the heap synchronously
		self.lock.acquire()
		delayed_function = heapq.heappop(self.delayed_functions)
		self.lock.release()
		return delayed_function

	def is_empty(self):
		return len(self.delayed_functions) == 0


class JobScheduler:
	def __init__(self):
		# The heap of delayed functions
		self.delayed_functions = DelayedFunctionsHeap()
		# The scheduler thread to execute delayed functions
		self.scheduler_thread = None
		# A lock that remains acquired by the main thread as long as the
		# scheduler remains active
		self.scheduler_stop_lock = threading.Lock()
		# A condition to put scheduler to sleep or to wake it up
		self.scheduler_awake = threading.Condition()
		# A flag as to whether the scheduler is accepting any more jobs
		self.open = True

	def _wait_scheduler(self):
		# print("Waiting for Scheduler")
		# Acquiring scheduler_awake => scheduler is asleep
		self.scheduler_awake.acquire()
		self.scheduler_awake.release()
		# print("Scheduler complete")

	def _wake_scheduler(self, blocking: bool):
		# Acquiring scheduler_awake => scheduler is asleep
		if (self.scheduler_thread is not None and 
				self.scheduler_awake.acquire(blocking=blocking)):
			# print("Waking up Scheduler")
			self.scheduler_awake.notify()
			self.scheduler_awake.release()

	def insert(self, f, n, *args, **kwargs):
		can_add = (
			# We can add if scheduler running and open to addition
			(self.scheduler_thread is not None and self.open)
			# or if scheduler not running
			or self.scheduler_thread is None
		)
		if can_add:
			# print("Adding scheduled function")
			# Adding the function to be executed with some delay
			self.delayed_functions.insert(n, f, *args, **kwargs)
			# Wake scheduler if needed
			self._wake_scheduler(blocking=False)
		else:
			# print("Scheduler is closed and not accepting more functions")
			pass

	def scheduler(self):
		# The scheduler function that executes functions with delay
		# Scheduler acquires lock on sleep condition as long as it has work
		self.scheduler_awake.acquire()
		# print("Scheduler has acquired lock")
		while True:
			# No more functions => Put scheduler to sleep to be woken later on
			if self.delayed_functions.is_empty():
				# print("Putting Scheduler to sleep")
				self.scheduler_awake.wait() # Releases lock on condition
			# Scheduler thread acquires scheduler_stop_lock => Terminate it
			if self.scheduler_stop_lock.acquire(blocking=False):
				# print("Breaking the Scheduler loop")
				self.scheduler_stop_lock.release()
				break
			# Pop the earliest function, sleep and execute it
			delay, func_with_args = self.delayed_functions.remove()
			sleep_time = max(0, delay - time.time() * 1000) / 1000
			# print(f"Scheduler Sleeping for {sleep_time} seconds")
			time.sleep(sleep_time)
			func_with_args()

	def start(self):
		# Acquires the scheduler stop lock as long as it must execute
		self.scheduler_stop_lock.acquire()
		if self.scheduler_thread is not None:
			# print("Scheduler already exists")
			pass
		else:
			# print("Starting Scheduler")
			self.scheduler_thread = threading.Thread(target=self.scheduler)
			self.scheduler_thread.start()

	def stop(self):
		# Close the heap to any further additions
		self.open=False
		# Wait for the scheduler to finish
		self._wait_scheduler()
		# Releasing scheduler_stop_lock => Scheduler can break its infinite loop
		self.scheduler_stop_lock.release()
		# Since the scheduler is asleep because it has no more work, wake it up
		# and let it kill itself
		self._wake_scheduler(blocking=True)
		self.scheduler_thread.join()
		# Reset scheduler thread
		self.scheduler_thread = None
		# print("Scheduler stopped")


# The test case for the scheduler involves adding things to  list
# and validating whether results are inserted in order
results = []
def useful_function(a: int, b: int):
	results.append(a ** b)

scheduler = JobScheduler()
scheduler.insert(useful_function, 1005, a=22, b=3)
scheduler.insert(useful_function, 2015, a=17, b=2)
scheduler.start()
scheduler.stop()
scheduler.insert(useful_function, 2015, a=77, b=2)
scheduler.insert(useful_function, 15, a=80, b=2)
scheduler.start()
scheduler.insert(useful_function, 3015, a=85, b=2)
scheduler.stop()

test_cases = [
	{
		"input": {
			"result": results
		},
		"output": [10648, 289, 6400, 5929, 7225]
	}
]


class ProblemSolver(Solver):
	def solve(self, input_value: dict):
		return input_value["result"]
