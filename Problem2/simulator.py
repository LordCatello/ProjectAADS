import Problem2


def main():
    aging_interval_choice_prompt = "Insert the amount of time slices after which a job waiting in the queue will have " \
                                   "" \
                                   "" \
                                   "" \
                                   "" \
                                   "" \
                                   "" \
                                   "its priority updated.\n" \
                                   "> "
    aging_interval = choose_positive_integer(aging_interval_choice_prompt)
    scheduler_choice = choose_scheduler()

    if scheduler_choice == 1:
        scheduler = Problem2.LazyJobScheduler(aging_interval)
    elif scheduler_choice == 2:
        scheduler = Problem2.ModuloJobScheduler(aging_interval)

    job_in_execution = None
    while True:
        if job_in_execution is not None:
            if job_in_execution.length > 0:
                job_in_execution.length -= 1
                print("Executing job {}. Time slices remaining: {}".format(job_in_execution.name,
                                                                           job_in_execution.length))
            else:
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

    job_name = input("Insert the name for this job:\n"
                     "> ")
    job_priority = choose_positive_integer("Insert the priority for this job:\n"
                                           "> ")
    job_length = choose_positive_integer("Insert the length for this job:\n"
                                         "> ")

    return job_name, job_priority, job_length


def choose_add_job() -> str:
    """Returns 'y' or 'n', if the user wants to add or not a job.
    The function loops until it gets valid input."""

    add_job_prompt = "Do you want to add a new job this time slice? (y/n)"
    error_string = "Insert only 'y' or 'n'.\n"
    user_input = input(add_job_prompt)
    while user_input not in ('y', 'n'):
        print(error_string)
        user_input = input(add_job_prompt)

    return user_input


def choose_positive_integer(prompt: str) -> int:
    """Returns a positive integer given by the user after a prompt.
    The function loops until it gets valid input."""

    error_string = "ERROR! Insert a valid positive number.\n"

    user_input = input(prompt)
    valid_input = True
    try:
        user_input = int(user_input)
    except ValueError:
        valid_input = False
    if valid_input and user_input < 1:
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
        if user_input < 1:
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
        Otherwise, a lazy job scheduler is usually the better choice.

        > """
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
