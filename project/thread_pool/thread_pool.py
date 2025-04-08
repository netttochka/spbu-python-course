import threading
from typing import Callable, Any, Tuple


class ThreadPool:
    """
    A simple thread pool implementation to manage and execute tasks concurrently.

    Attributes:
        num_threads (int): The number of threads in the pool.
        tasks (list): A queue of tasks to be executed by the threads.
        threads (list): List of active threads in the pool.
        shutdown_flag (bool): A flag to indicate when the thread pool should be shut down.
        lock (threading.Lock): A lock to synchronize access to the task queue.
        task_available (threading.Condition): A condition variable to signal threads when tasks are available.
    """

    def __init__(self, num_threads: int):
        """
        Initializes the thread pool with a specified number of threads.

        Args:
            num_threads (int): Number of threads in the pool.
        """
        self.num_threads: int = num_threads
        self.tasks: list[
            Tuple[Callable, Tuple[Any, ...], dict[str, Any]]
        ] = []  # Queue of tasks (task, args, kwargs)
        self.threads: list[threading.Thread] = []  # List of threads
        self.shutdown_flag: bool = False  # Flag to indicate shutdown
        self.lock: threading.Lock = threading.Lock()  # Lock for thread synchronization
        self.task_available: threading.Condition = threading.Condition(
            self.lock
        )  # Condition variable

        # Start threads
        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker)
            thread.start()
            self.threads.append(thread)

    def _worker(self):
        """
        Worker thread that continuously fetches and executes tasks from the queue.
        This method runs in an infinite loop until a shutdown is triggered.
        """
        while True:
            with self.task_available:
                # Wait for tasks to become available or for shutdown
                while not self.tasks and not self.shutdown_flag:
                    self.task_available.wait()

                # Exit if shutdown has been triggered and no tasks are remaining
                if self.shutdown_flag and not self.tasks:
                    break

            # Safely pop the next task from the queue using the lock
            with self.lock:
                if self.tasks:
                    task, args, kwargs = self.tasks.pop(0)
                else:
                    continue  # If the task queue is empty, skip to the next iteration

            # Execute the task
            task(*args, **kwargs)

    def enqueue(self, task: Callable, *args: Any, **kwargs: Any):
        """
        Enqueues a task to be executed by the thread pool.

        Args:
            task (Callable): The task function to be executed.
            *args (Any): Positional arguments to pass to the task.
            **kwargs (Any): Keyword arguments to pass to the task.
        """
        with self.task_available:
            self.tasks.append((task, args, kwargs))  # Add task to the queue
            self.task_available.notify()  # Notify a worker thread

    def dispose(self):
        """
        Signals the thread pool to shut down. This will stop accepting new tasks,
        but existing tasks will still be executed.
        """
        with self.task_available:
            self.shutdown_flag = True  # Set shutdown flag
            self.task_available.notify_all()  # Wake up all worker threads

        # Wait for all threads to finish their work
        for thread in self.threads:
            thread.join()
