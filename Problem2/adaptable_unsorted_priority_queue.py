from Problem2.dependencies.list.positional_list import PositionalList


class TimeScheduler:

    # -------------------------------- Nested Job class --------------------------------

    class _Job:
        __slots__ = 'priority', 'length', 'arrival_time'

        def __init__(self, priority: int, length: int, arrival_time: int):
            """
            Creates a new job to be scheduled. This should not be constructed by the user.

            :param priority: The priority of this job. It must be an integer in the range [-20, 19], inclusive, where the
            highest priority is represented by the lowest number and vice versa.
            :param length: The number of time slices this job will be executed for.
            :param arrival_time: The number of the time slice this job was created.
            """
            if not (-20 <= priority <= 19):
                raise ValueError("Priority must be between -20 and 19.")

            self.priority = priority
            self.length = length
            self.arrival_time = arrival_time

    __slots__ = '_priority_queue', '_current_time'

    def __init__(self):
        """Creates an empty TimeScheduler, ready to receive jobs."""
        self._priority_queue = PositionalList()
        self._current_time = 0

    def _increment_time(self):
        self._current_time += 1

    def add_job(self, priority: int, length: int):
        job_to_add = self._Job(priority, length, self._current_time)








