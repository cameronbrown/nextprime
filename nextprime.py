from math import sqrt, floor, ceil, log
import argparse

parser = argparse.ArgumentParser(
    description="Find first prime number greater than target integer N."
)
parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="output debugging messages",
)
target_or_test = parser.add_mutually_exclusive_group(required=True)
target_or_test.add_argument(
    "target",
    nargs="?",
    metavar="N",
    type=int,
    help="where to start search for next prime",
)
target_or_test.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="do some tests",
)

args = parser.parse_args()


def debug(msg: str) -> None:
    if args.debug or args.test:
        print(msg)


def is_odd(n: int) -> bool:
    return bool(n % 2)


def expected_prime_distance(n: int) -> int:
    """
    Returns expected distance between primes at n
    :param n: int
    :return: int
    """
    # According to prime number theorem, expected density of primes around n
    # is 1 / ln(n).  So for an average we should expect primes to be about ln(n)
    # integers apart.
    return int(ceil(log(n)))


def next_prime(n: int) -> int:
    """
    Returns next prime number after n
    :param n: int
    """
    if n < 2:
        # Easy. First prime is 2
        return 2

    # Algorithm assumes an even n.  We can safely use n+1 as a basis
    # when n is odd and >2 (even numbers >2 can never be prime)
    if is_odd(n):
        n += 1

    # Examine a range of 2 * expected_prime_distance(n) integers after n.
    # Identify all non-primes in range. If nothing in range is prime,
    # increment n to last checked integer and repeat. Because primes
    # are expected to be found roughly every expected_prime_distance
    # we shouldn't have to repeat loop very many times.
    while True:
        sqrt_n: int = int(floor(sqrt(n)))
        test_factors = range(3, sqrt_n + 1, 2)
        testing_range: int = 2 * expected_prime_distance(n)
        test_offsets = range(1, testing_range, 2)
        non_prime_offsets: set[int] = set()

        debug(f"   Looking for prime in range of {testing_range} following target")
        debug(f"   Using {len(test_factors)} test factors to find non-primes in range")

        for test_factor in test_factors:
            factor_remainder = n % test_factor
            next_multiple_offset_from_n = test_factor - factor_remainder
            if not is_odd(next_multiple_offset_from_n):
                next_multiple_offset_from_n += test_factor
            while next_multiple_offset_from_n < testing_range:
                non_prime_offsets.add(next_multiple_offset_from_n)
                next_multiple_offset_from_n += 2 * test_factor

        debug(f"   Added {len(non_prime_offsets)} non-prime offsets:")
        debug(f"     {sorted(non_prime_offsets)}")

        last_offset = 0
        for test_offset in test_offsets:
            if test_offset not in non_prime_offsets:
                debug(f"   Found prime at offset {test_offset}")
                return n + test_offset
            last_offset = test_offset

        # No primes found in range. Search a new range of integers
        # starting where we left off.
        debug(f"   No primes found from {n} to {n + last_offset}.")
        n += last_offset + 1  # start n at first even int after last checked
        debug(f"   Now looking for primes from {n} to {n + last_offset}.")


def is_prime_by_trial_division(n: int) -> int:
    for divisor in range(3, int(sqrt(n)), 2):
        if n % divisor == 0:
            return divisor
    return 0


def test_small_ns():
    assert next_prime(0) == 2
    assert next_prime(100) == 101
    assert next_prime(101) == 103
    assert next_prime(1000) == 1009


def test_large_ns():
    assert next_prime(101_537) == 101_561
    assert next_prime(1_000_000_014_749) == 1_000_000_014_833


SOME_TEST_CASES = [
    (0, 2),
    (100, 101),
    (101, 103),
    (1000, 1009),
    (101_537, 101_561),
    (1_000_000_014_749, 1_000_000_014_833),
]


def verbose_tests():
    for n, nxt in SOME_TEST_CASES:
        debug(f"Finding next prime number after {n}. Expecting {nxt}")
        np = next_prime(n)
        debug(f"next_prime({n}) => {np}: {'PASS' if np == nxt else 'FAIL'}")
        if np != nxt:
            debug(f"divisor of {np} is: {is_prime_by_trial_division(np)}")


if __name__ == "__main__":
    if args.test:
        verbose_tests()
    else:
        print(next_prime(args.target))
