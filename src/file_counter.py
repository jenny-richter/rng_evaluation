#!/usr/bin/env python
import os
# import time

counter_file_path = "~/Projekte/python/rng_evaluation/counter.txt"
last_run_file_path = "~/Projekte/python/rng_evaluation/src/download.py"


# def is_cron_restarted():
#     current_time = int(time.time())
#     if os.path.isfile(last_run_file_path):
#         with open(last_run_file_path, "r") as f:
#             last_run = int(f.read().strip())
#         # Wenn mehr als 5 Minuten vergangen sind --> Cron-Job neu gestartet wurde
#         if current_time - last_run > 300:
#             return True
#     with open(last_run_file_path, "w") as f:
#         f.write(str(current_time))
#     return False


def read_counter_from_file():
    if os.path.isfile(counter_file_path):
        with open(counter_file_path, "r") as f:
            counter = int(
                f.read().strip()
            )  # Strip whitespaces and tabs & reads the file in Strings
    else:
        counter = 0
    return counter


def write_counter_to_file(counter):
    with open(counter_file_path, "w") as f:
        f.write(str(counter))


def increment():
    counter = read_counter_from_file()
    new_counter = counter + 1
    write_counter_to_file(new_counter)
    return new_counter


if __name__ == "__main__":
    increment()
