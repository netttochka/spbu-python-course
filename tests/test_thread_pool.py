from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from project.thread_pool.thread_pool import ThreadPool
from project.thread_pool.parallel_cartesian_sum import parallel_cartesian_sum
import time
import pytest
import threading

# Example task
def example_task(x, results):
    time.sleep(1)  # Simulating task execution
    results.append(x)


def test_num_threads():
    pool = ThreadPool(3)
    # Check if the active thread count is as expected (including the main thread)
    expected_active_threads = 3 + 1  # +1 for the main thread
    assert (
        threading.active_count() == expected_active_threads
    ), f"Expected {expected_active_threads} active threads, but got {threading.active_count()}"
    pool.dispose()


def test_thread_disposal():
    pool = ThreadPool(3)
    results = []

    # Add tasks to the pool
    for i in range(3):
        pool.enqueue(example_task, i, results)

    # Ensure that the threads have started working
    time.sleep(0.5)  # Allow some time for threads to start working
    assert len(results) == 0, "Threads should not be done yet"

    # Dispose of the pool
    pool.dispose()

    # Verify that the tasks have been completed
    assert len(results) == 3, "Not all tasks finished after dispose"


def test_enqueue_and_execute():
    pool = ThreadPool(3)
    results = []

    start_time = time.time()

    # Add tasks to the pool
    for i in range(6):
        pool.enqueue(example_task, i, results)

    pool.dispose()

    end_time = time.time()

    # Ensure the tasks were executed in parallel (execution time should ideally be around 2 seconds, but allow up to 3 seconds due to potential delays)
    assert sorted(results) == [
        0,
        1,
        2,
        3,
        4,
        5,
    ], "Tasks did not execute in the expected order"
    assert (
        end_time - start_time < 3
    ), "Tasks were not executed in parallel (execution took too long)"


@pytest.mark.parametrize(
    "expected_sum, list_of_sets",
    [(33, [{22}, {11}]), (20, [{1, 2}, {3, 4}]), (84, [{1, 2}, {3, 4}, {5, 6}])],
)
def test_parallel_cartesian_sum(expected_sum, list_of_sets):
    # Test parallel Cartesian sum calculation
    assert expected_sum == parallel_cartesian_sum(list_of_sets)
