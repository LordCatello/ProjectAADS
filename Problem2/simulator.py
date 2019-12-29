from typing import Callable

from . import *  # relative imports are contained in __init__.py

PROMPT_SYMBOL = "> "


def main():
    aging_interval_choice_prompt = "Insert the amount of time slices after which a job waiting in the queue will" \
                                   " have its priority updated.\n" + PROMPT_SYMBOL
    aging_interval = choose_positive_integer(aging_interval_choice_prompt)
    scheduler_choice = choose_scheduler()

    if scheduler_choice == 1:
        scheduler = LazyJobScheduler(aging_interval)
    elif scheduler_choice == 2:
        scheduler = ModuloJobScheduler(aging_interval)

    job_in_execution = None
    while True:
        if job_in_execution is not None:
            if job_in_execution.length > 1:
                job_in_execution.length -= 1
                print("Executing job {}. Time slices remaining: {}".format(job_in_execution.name,
                                                                           job_in_execution.length))
            else:
                print("Finishing job {}. No time slices remaining.".format(job_in_execution.name))
                job_in_execution = None

        add_job_choice = choose_add_job()

        if add_job_choice == 'y':
            name, priority, length = ask_job()
            scheduler.add_job(name, priority, length)  # need to check for bad creation

        if job_in_execution is None:
            job_in_execution = scheduler.get_max_priority_job()
        scheduler.increment_time()


def ask_job() -> (str, int, int):
    """Asks the user for a tuple of name, priority, length of a job.
    It then returns this information.
    The function loops until it gets valid input."""

    job_name = input("Insert the name for this job:\n" + PROMPT_SYMBOL)
    job_priority = choose_priority()
    job_length = choose_length()

    return job_name, job_priority, job_length


def choose_add_job() -> str:
    """Returns 'y' or 'n', if the user wants to add or not a job.
    The function loops until it gets valid input."""

    add_job_prompt = "Do you want to add a new job this time slice? (y/n)\n" + PROMPT_SYMBOL
    error_string = "Insert only 'y' or 'n'.\n"
    user_input = input(add_job_prompt)
    while user_input not in ('y', 'n'):
        print(error_string)
        user_input = input(add_job_prompt)

    return user_input


def choose_priority() -> int:
    """Returns a valid priority number given by the user.
    The function loops until it gets valid input."""
    max_priority = BaseJobScheduler.Job.MAX_PRIORITY
    min_priority = BaseJobScheduler.Job.MIN_PRIORITY
    priority_error_string = "Insert a number between {} and {}.".format(max_priority, min_priority)
    priority_check = lambda integer: max_priority <= integer <= min_priority

    return choose_integer("Insert the priority for this job:\n"
                          + PROMPT_SYMBOL, priority_error_string, priority_check)


def choose_length() -> int:
    """Returns a valid length number given by the user.
    The function loops until it gets valid input."""

    min_length = BaseJobScheduler.Job.MIN_LENGTH
    max_length = BaseJobScheduler.Job.MAX_LENGTH
    length_error_string = "Insert a number between {} and {}.".format(min_length, max_length)
    length_check = lambda integer: min_length <= integer <= max_length

    return choose_integer("Insert the length for this job:\n"
                          + PROMPT_SYMBOL, length_error_string, length_check)


def choose_positive_integer(prompt: str) -> int:
    """Returns a positive integer given by the user.
    The function loops until it gets valid input."""

    return choose_integer(prompt, "Please insert a positive integer.",
                          lambda integer: integer > 0)


def choose_integer(prompt: str, error_string: str, is_valid: Callable[[int], bool]) -> int:
    """Returns an integer which respects a certain condition given by the user.
    The function loops until it gets valid input.

    :param prompt: The string to be displayed to the user to get the input.
    :param error_string: The string to be displayed in case of invalid input.
    :param is_valid: A callable object which takes an integer and returns a boolean value, used to validate the input.
    """

    user_input = input(prompt)
    valid_input = True
    try:
        user_input = int(user_input)
    except ValueError:
        valid_input = False
    if valid_input and not is_valid(user_input):
        valid_input = False

    while not valid_input:
        valid_input = True
        print(error_string)
        user_input = input(prompt)
        try:
            user_input = int(user_input)
        except ValueError:
            valid_input = False
            continue
        if not is_valid(user_input):
            valid_input = False

    return user_input


def choose_scheduler() -> int:
    """Returns 1 if the choice is a LazyJobScheduler, 2 if it is a ModuloJobScheduler.
    If the user input is not one of 1 or 2, the function loops until it gets valid input."""

    scheduler_choice_prompt = """Do you wish to use a lazy job scheduler (1) or a modulo job scheduler (2)?

        Note: a lazy job scheduler updates priorities only when a new job is requested, whereas a modulo job scheduler
        does it at every time slice, but only on a subset of the jobs.

        Use a modulo job scheduler if you know that the aging interval of a job is very high compared to the average 
        length
        of the jobs, and if you know that the distribution in time of the jobs will be uniform.
        Otherwise, a lazy job scheduler is usually the better choice.\n\n""" + PROMPT_SYMBOL
    error_string = "ERROR! Please insert a 1 or a 2.\n"

    user_input = input(scheduler_choice_prompt)
    try:
        user_input = int(user_input)
    except ValueError:
        print(error_string)

    while user_input not in (1, 2):
        user_input = input(scheduler_choice_prompt)
        try:
            user_input = int(user_input)
        except ValueError:
            print(error_string)

    return user_input


# Command line usage
if __name__ == '__main__':
    main()
