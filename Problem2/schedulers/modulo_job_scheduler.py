from typing import Optional

from .base_job_scheduler import BaseJobScheduler
from ..dependencies.array_map import ArrayMap
from ..dependencies.priority_queue.adaptable_heap_priority_queue import AdaptableHeapPriorityQueue


class ModuloJobScheduler(BaseJobScheduler):
    """
    A scheduler for handling jobs using priorities. It supports aging, updating priorities at every time slice.
    It does not visit all the jobs, though, but only the ones that could be updated given the current time and the
    aging interval.

    Moreover, only the jobs which arrived in an arrival_time which is congruent to 0 modulo aging_interval can be
    updated, so only these ones are visited.
    Therefore, a separate data structure based on arrival times is held to update priorities, and a heap-based
    adaptable priority queue is used for getting the highest priority job.
    """
    __slots__ = '_current_time', '_priority_queue', '_aging_interval', '_jobs_by_modulo_aging_interval', '_size'

    def __init__(self, aging_interval: int):
        """
        Creates an empty ModuloJobScheduler, ready to receive jobs.

        :param aging_interval:
            The number of time slices after which a job waiting in the queue has its priority increased, in order to
            avoid starving of jobs.
        """
        self._current_time = 0
        self._priority_queue = AdaptableHeapPriorityQueue()
        self._aging_interval = aging_interval
        self._size = 0
        # This maps the arrival time modulo aging_interval to all the Locator objects which are congruent to the
        # definition. The Locator object finds the element in the priority queue, in order to access the element in
        # O(1) when the priority will be updated.
        self._jobs_by_modulo_aging_interval = ArrayMap(aging_interval)

        # To simulate a MultiMap, the values of the map will simply be lists of job Locators.
        for key in self._jobs_by_modulo_aging_interval:
            self._jobs_by_modulo_aging_interval[key] = []

    def increment_time(self):
        """Must be called at every time slice.
        It performs an update on the priority of the jobs which waited too much by visiting the jobs which arrived in
        a time which is congruent to 0 modulo aging_interval."""
        self._current_time += 1  # beware off-by-one errors!
        self._update_priorities()

    def _update_priorities(self):
        updatable_time = self._current_time % self._aging_interval
        updatable_jobs_locators = self._jobs_by_modulo_aging_interval[updatable_time]

        for job_locator in updatable_jobs_locators:
            # couldn't find a public method to unwrap a locator, and didn't want to store locator AND value when the
            # locator stores the value already.
            job = job_locator._value

            # since we are already visiting the jobs which arrived in a time which is congruent to 0 modulo
            # aging_interval,
            # if the current time is greater than the arrival I am sure I need to update the priority of the job.
            # Moreover, I am also sure I need to update it of only one because this method is called at each time slice.
            if self._current_time > job.arrival_time:
                job.priority -= 1
                # ensuring it doesn't get below the minimum
                if job.priority < BaseJobScheduler.Job.MAX_PRIORITY:
                    job.priority = BaseJobScheduler.Job.MAX_PRIORITY

                # updating the queue
                self._priority_queue.update(job_locator, job.priority, job)

    def add_job(self, name: str, priority: int, length: int):
        job_to_add = self.Job(name, priority, length, self._current_time)
        job_locator = self._priority_queue.add(priority, job_to_add)
        self._jobs_by_modulo_aging_interval[self._current_time % self._aging_interval].append(job_locator)
        self._size += 1

    def get_max_priority_job(self) -> Optional[BaseJobScheduler.Job]:
        """
        Gives the highest priority job and removes it from the job queue.
        Warning: this method expects the jobs to be already updated, so it should be called after increment_time.

        :return: the highest priority job or None if no jobs are present in the queue.
        """

        if self._size <= 0:
            return None

        priority_job = self._priority_queue.remove_min()[1]

        # ----- find the job to remove in the helping data structure and delete it -----

        job_locators_to_visit = self._jobs_by_modulo_aging_interval[priority_job.arrival_time % self._aging_interval]

        for index, job_locator in enumerate(job_locators_to_visit):
            # couldn't find a public method to unwrap a locator, and didn't want to store locator AND value when the
            # locator stores the value already.
            job = job_locator._value

            if job == priority_job:
                # am i really sure it will always find it in this way?
                index_to_delete = index
                break

        job_locators_to_visit.pop(index_to_delete)

        self._size -= 1
        return priority_job
