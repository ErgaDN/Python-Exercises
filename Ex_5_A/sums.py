import heapq


def sorted_subset_sums(numbers):
    """

    Generate all subset sums of the input list of numbers in sorted order.

    :param numbers: List of integers.
    :return: Generator of sorted subset sums.

    >>> import itertools
    >>> from itertools import takewhile, islice, pairwise

    >>> list(sorted_subset_sums([]))
    [0]

    >>> list(sorted_subset_sums([1]))
    [0, 1]

    >>> for i in sorted_subset_sums([1,2,4]): print(i, end=", ")
    0, 1, 2, 3, 4, 5, 6, 7,

    >>> list(sorted_subset_sums([1,2,3]))
    [0, 1, 2, 3, 3, 4, 5, 6]

    >>> list(sorted_subset_sums([2,3,4]))
    [0, 2, 3, 4, 5, 6, 7, 9]

    >>> list(islice(sorted_subset_sums(range(100)),5))
    [0, 0, 1, 1, 2]

    >>> list(takewhile(lambda x:x<=6, sorted_subset_sums(range(1,100))))
    [0, 1, 2, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6]

    >>> list(zip(range(5), sorted_subset_sums(range(100))))
    [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]

    >>> len(list(takewhile(lambda x : x <= 1000, sorted_subset_sums(list(range(90,100)) + list(range(920,1000))))))
    1104

    >>> list(sorted_subset_sums([2, 4, 8, 16]))
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]

    >>> len(list(sorted_subset_sums(range(1, 10))))
    512

    >>> max(list(sorted_subset_sums([10, 20, 30, 40])))
    100

    >>> all(x <= y for x, y in pairwise(sorted_subset_sums(range(1, 20))))
    True

    """

    # Handle the special case where the input list is empty
    if not numbers:
        yield 0
        return

    # Sort the input numbers to ensure subsets are processed in order
    numbers = sorted(numbers)

    # Initialize the min-heap with the sum of the empty subset (0) and starting index (0)
    heap = [(0, 0)]  # (current_sum, index)

    while heap:
        # Pop the smallest sum from the heap
        current_sum, index = heapq.heappop(heap)
        yield current_sum

        # Generate new sums by adding each subsequent number to the current sum
        for i in range(index, len(numbers)):
            new_sum = current_sum + numbers[i]
            heapq.heappush(heap, (new_sum, i + 1))


if __name__ == '__main__':
    from itertools import takewhile, islice

    for i in eval(input()):
        print(i, end=", ")
