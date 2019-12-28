from .base_job_scheduler import BaseJobScheduler
from ..dependencies.list.positional_list import PositionalList


class LazyJobScheduler(BaseJobScheduler):
    """
    A scheduler for handling jobs, using priorities and aging.
    It handles everything only when a new job is requested, and not every time slice.
    """

    __slots__ = '_priority_queue', '_current_time', '_aging_interval'

    def __init__(self, aging_interval):
        """
        Creates an empty LazyJobScheduler, ready to receive jobs.

        :param aging_interval:
            The number of time slices after which a job waiting in the queue has its priority increased, in order to
            avoid starving of jobs.
        """
        self._priority_queue = PositionalList()
        self._current_time = 0
        self._aging_interval = aging_interval

    def increment_time(self):
        """Since a LazyJobScheduler only operates every once in a while, it needs to know when a time slice has
        passed in some way.
        Call this method when a time slice passes."""
        self._current_time += 1

    def add_job(self, priority: int, length: int):
        """Adds a new job to the queue with the specified priority and length."""
        job_to_add = self.Job(priority, length, self._current_time)
        self._priority_queue.add_last(job_to_add)

    def get_max_priority_job(self) -> BaseJobScheduler.Job:
        """
        Gives the highest priority job to be scheduled.
        Moreover, it updates the queue, aging the jobs which waited too long, according to the aging_interval
        parameter. It then returns the job with the highest priority up to date, removing it from the job queue.

        The update is only made when a job is requested, so it should not be performed when a job is being executed
        by the processor.


        :return:
            The job with the highest priority after the update."""
        priority_job_position = self._priority_queue.first()

        # I can't iterate with __iter__ because PositionalList returns an iterator over elements, when I want to keep
        #  track of where the job is stored in the list, in order to remove it at the end in O(1).
        current_job_position = priority_job_position
        while current_job_position is not None:
            current_job = current_job_position.element()

            # Update the job priority and arrival time if needed
            self._age_job(current_job)

            # Finding the maximum priority job (max priority = -20)
            if current_job.priority < priority_job_position.element().priority:
                priority_job_position = current_job_position

            # updating next element to iterate over
            current_job_position = self._priority_queue.after(current_job_position)

        return self._priority_queue.delete(priority_job_position)

    def _age_job(self, job: BaseJobScheduler.Job):
        """If a job has waited enough time, as specified in the aging_interval parameter, the job has its priority
        and its arrival time updated.
        The two will be updated according to how many aging intervals the job has waited in the queue with respect to
        the current time.

        If a job has not been in the queue for enough time, it will not be updated."""
        waiting_time = self._current_time - job.arrival_time
        age_increment = waiting_time // self._aging_interval

        # if a job needs to age, I update its priority and its arrival time for future updates
        if age_increment > 0:
            job.priority += age_increment
            job.arrival_time += self._aging_interval * age_increment
