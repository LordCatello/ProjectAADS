from abc import abstractmethod


class BaseJobScheduler:
    """An abstract base class for job schedulers."""

    # -------------------------------- Nested Job class --------------------------------

    class Job:
        """
        A job for the processor. It has an associated priority and length - the duration in time slices the processor
        will need to complete it.
        Since the environment of the job supports aging, the arrival time of the job is kept track of.
        """
        __slots__ = 'priority', 'length', 'arrival_time'

        MAX_PRIORITY = -20
        MIN_PRIORITY = 19

        def __init__(self, priority: int, length: int, arrival_time: int):
            """
            Creates a new job to be scheduled. This should not be constructed by the user.

            :param priority:
                The priority of this job. It must be an integer in the range [-20, 19], inclusive, where the highest
                priority is represented by the lowest number and vice versa.
            :param length:
                The number of time slices this job will be executed for.
            :param arrival_time:
                The number of the time slice this job was created.
            """
            if not (BaseJobScheduler.Job.MAX_PRIORITY <= priority <= BaseJobScheduler.Job.MIN_PRIORITY):
                raise ValueError("Priority must be between {} and {}.".format(BaseJobScheduler.Job.MAX_PRIORITY,
                                                                              BaseJobScheduler.Job.MIN_PRIORITY))

            self.priority = priority
            self.length = length
            self.arrival_time = arrival_time

    @abstractmethod
    def get_max_priority_job(self) -> Job:
        raise NotImplementedError("Must be implemented by subclasses.")

    @abstractmethod
    def add_job(self, priority: int, length: int):
        raise NotImplementedError("Must be implemented by subclasses.")

    @abstractmethod
    def increment_time(self):
        """Call this method at every time slice."""
        raise NotImplementedError("Must be implemented by subclasses.")
