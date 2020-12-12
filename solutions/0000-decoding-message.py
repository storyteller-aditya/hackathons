# Given the mapping a=1, b=2, ..., z=26 and an encoded message, count
# the number of ways in which it can be decoded.
# Example: 111 can be decoded as aaa or ak or ka. Therefore the output
# should be 3. 
# You can assume that all messages are decodable.

# Approach:
# Let C(k) be the count of the number of ways upto index k of the string.
# Since the mapping can at most be a two digit number, it is apt to attempt
# to calculate C(k+2) assuming C(k) and C(k+1) has been computed because
# two possible cases can exist:
# - If the string has been decoded till the kth index and string[k+1] and
#   string[k+2] combined is valid, then we must include a contribution of
#   C(k) towards C(k+2)
# - If the string has been decoded till the k+1th index and string[k+2] is 
#   valid, then we must include a contribution of C(k+1) towards C(k+2)
# This can be put mathematically as:
# C(k+2) = (
#     C(k) * [1 if string[k+1] and string[k+2] are together valid else 0]
#     + C(k+1) * [1 if string[k+2] is individually valid else 0]
# )
# Thereafter we can iterate through the string, computing C(k+2) from the
# prior two existing values.

from components import Solver


test_cases = [
    {
        "input": {
            "string": "111"
        },
        "output": 3
    },
    {
        "input": {
            "string": "111111"
        },
        "output": 13
    }
]


def get_count_k_plus_2(substring: str, count_k: int, count_k_plus_1: int):
    """
    Given a string, calculates C(k+2) from C(k+1) and C(k)
    using the above mentioned formula
    :param substring: The input string
    :param count_k: The current C(k)
    :param count_k_plus_1: The current C(k+1)
    :return: The new value of C(k+2)
    """
    count_k_plus_2 = 0
    # If both digits together are valid then that is one way to decode
    if int(substring) < 27:
        count_k_plus_2 += count_k
    # If second digit is larger than zero, then both digits separate
    # is another way to decode
    if int(substring[1]) > 0:
        count_k_plus_2 += count_k_plus_1
    return count_k_plus_2


def ways_to_decode_message(string: str) -> int:
    """
    Returns the number of ways to decode a message using the above algorithm
    :param string: The input string
    :return: The number of ways that it can be decoded
    """
    # Handles the base case where the string is 1 digit long
    count_k = 1
    if len(string) == 1:
        return count_k
    # Handles the base case where the string is 2 digits long
    # We can use the same function get_count_k_plus_2 with both count args
    # equal to 1 because there are at most two ways to decode a string
    # upto its first two digits and this function performs the necessary checks
    count_k_plus_1 = get_count_k_plus_2(string[:2], count_k=1, 
                                        count_k_plus_1=1)
    if len(string) == 2:
        return count_k_plus_1
    # Handles all other cases with the iterative algorithm
    for k in range(len(string) - 2):
        count_k_plus_2 = get_count_k_plus_2(string[k+1:k+3], count_k=count_k, 
                                            count_k_plus_1=count_k_plus_1)
        # Update the counts for the next k
        count_k = count_k_plus_1
        count_k_plus_1 = count_k_plus_2
    return count_k_plus_2


class ProblemSolver(Solver):
    def solve(self, input_value: dict):
        return ways_to_decode_message(input_value["string"])