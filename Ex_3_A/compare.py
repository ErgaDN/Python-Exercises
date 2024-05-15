import numpy as np
import scipy as sc
from numpy.linalg import solve
from time import perf_counter
import matplotlib.pyplot as plt


def solve_with_root(a: np.ndarray, b: np.ndarray):
    """
        Solves a system of linear equations using scipy.optimize.root.

        Parameters:
            a (np.ndarray): Coefficient matrix.
            b (np.ndarray): Constant vector.

        Returns:
            np.ndarray: Solution vector x such that a @ x = b.

        Example:
        >>> solve_with_root(np.array([[1, 2], [3, 5]]), np.array([1, 2]))
        array([-1.,  1.])

        >>> solve_with_root(np.array([[2, 3, 1], [1, 1, 1], [1, -1, 2]]), np.array([10, 6, 5]))
        array([-2.,  3.,  5.])
        """

    def equations(x):
        return a @ x - b

    solution = sc.optimize.root(equations, np.zeros(a.shape[1]))
    return solution.x


def test_solve_with_root():
    """
    Test function for solve_with_root.

    This function generates random inputs for a system of linear equations,
    solves it using both solve_with_root and numpy.linalg.solve, and compares the results.

    >>> test_solve_with_root()
    All tests passed!
    """

    # Number of test cases
    num_tests = 1000
    # Size of matrices
    matrix_size = 50

    for _ in range(num_tests):
        # Generate random coefficient matrix and constant vector
        a = np.random.randint(-100, 100, size=(matrix_size, matrix_size))
        b = np.random.randint(-100, 100, size=matrix_size)

        # Solve using solve_with_root
        root_solution = solve_with_root(a, b)

        # Solve using numpy.linalg.solve
        numpy_solution = solve(a, b)

        # Check if solutions are close
        assert np.allclose(root_solution, numpy_solution), "Test failed."
    print("All tests passed!")


def measure_time(func, *args, **kwargs):
    """
        Measure the time it takes to execute a function.

        Parameters:
            func (callable): The function to measure.
            *args: Variable length argument list for the function.
            **kwargs: Arbitrary keyword arguments for the function.

        Returns:
            float: The time taken to execute the function in seconds.

        Example:
        >>> def sample_function(x):
        ...     return x**2
        >>> measure_time(sample_function, 2) < 1
        True
        """

    start = perf_counter()
    result = func(*args, **kwargs)
    end = perf_counter()
    return end - start


def compare_solution_methods():
    """
        Compare the performance of solve_with_root and numpy.linalg.solve on random inputs of different sizes.

        Generates random coefficient matrices and constant vectors of sizes between 1 and 1000,
        measures the execution time for both solve_with_root and numpy.linalg.solve, and plots the results.

        The function generates a plot saved as 'comparison.png' and also displays it.

        Example:
        >>> compare_solution_methods()  # This will generate and show a plot
        """
    sizes = list(range(1, 301))
    root_times = []
    numpy_times = []

    for size in sizes:
        # Generate random coefficient matrix and constant vector
        a = np.random.randint(-1000, 1000, size=(size, size))
        b = np.random.randint(-1000, 1000, size=size)

        # Measure time for solve_with_root
        root_times.append(measure_time(solve_with_root, a, b))
        numpy_times.append(measure_time(solve, a, b))

    # Plot the results
    plt.plot(sizes, root_times, label='solve_with_root')
    plt.plot(sizes, numpy_times, label='numpy.linalg.solve')
    plt.xlabel('Input Size')
    plt.ylabel('Average Running Time (s)')
    plt.title('Performance Comparison')
    plt.legend()
    plt.savefig("comparison.png")  # after you plot the graphs, save them to a file and upload it separately.
    plt.show()  # this should show the plot on your screen


if __name__ == '__main__':
    # put your code here
    test_solve_with_root()
    compare_solution_methods()

    # a = np.array([[1, 2], [3, 5]])
    # b = np.array([1, 2])
    # x = np.linalg.solve(a, b)

    # print(solve_with_root(np.array([[1, 2], [3, 5]]), np.array([1, 2])))
    # compare_solution_methods()
    # print(solve_with_root(np.array([[2, 3, 1], [1, 1, 1], [1, -1, 2]]), np.array([10, 6, 5])))


