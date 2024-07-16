#!/usr/bin/env python
import csv
import os


def count_success_failure(directories, path):
    success = 0
    failure = 0
    base_path = path
    for dir in directories:
        stats_path = os.path.join(base_path, dir, "stats.txt")
        with open(stats_path, "r") as file:
            for line in file:
                success += line.lower().count("success")
                failure += line.lower().count("failure")
    return success, failure


def write_results_to_csv(file_path, csv_file_path, file_exists, success, failure, total_tests, passed_tests_summary, failed_tests_summary ):
    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                ["Filename", "Final result", "File Size (MB)", "Sucsess", "Failure", "total_tests","passed_tests", "failed_tests_summary", "passed_test_summerary"]
            )

    filename = os.path.basename(file_path)
    if failure==0:
        final_result = "random"
    else:
        final_result = "not random"
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024**2)

    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                filename,
                final_result,
                round(file_size_mb, 2),
                success,
                failure,
            ]
        )
    print(f"For File: {filename}, File Size: {round(file_size_mb, 2)} MB")


def process_and_write_results(binary_file, directories, path, csv_file_path):
    success, failure = count_success_failure(directories, path)

    print("Success: ", success, " Failure: ", failure)

    file_exists = os.path.isfile(csv_file_path)
    write_results_to_csv(binary_file, csv_file_path, file_exists, success, failure)
