#!/usr/bin/env python3
import os
import shutil
import subprocess
import random
import sys
import time
from csv_writer_nist_results import process_and_write_results
from helper import load_config


# funktion to execute a command for statistical analysis
def sts(file_path, dir):
    verbose_level = 1
    instance = 1
    work_dir = dir
    file_format = "r"
    mode = "b"

    change_Parameters = "1=20000,2=10,3=9,4=8,5=16,6=1000,7=1073,9=1000000"
    config = load_config("./configuration/local.yaml")
    sts_legacy_path = config["paths"]["sts_legacy_fft_directory"]

    command = [
        sts_legacy_path,
        "-v",
        str(verbose_level),
        "-I",
        str(instance),
        "-P",
        change_Parameters,
        "-w",
        work_dir,
        "-F",
        file_format,
        "-m",
        mode,
        "-s",
        file_path,
    ]

    # debugging information
    print("current working directory:", os.getcwd())
    full_command_path = os.path.abspath(command[0])
    print("complete path to sts_legacy_fft:", full_command_path)

    if not os.path.exists(full_command_path):
        print(f"executable file not found:{full_command_path}")
        return

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error executing the command:{e}")
    except FileNotFoundError as e:
        print(f"file not found error: {e}")


# creating a temporary folder and a result subfolder
def create_tmp_and_result_folders(base_path=".", tmp_folder_name="tmp"):
    tmp_folder_path = os.path.join(base_path, tmp_folder_name)
    if not os.path.exists(tmp_folder_path):
        os.makedirs(tmp_folder_path)
    for i in range(1, 11):
        result_folder_path = os.path.join(tmp_folder_path, f"result_{i}")
        if not os.path.exists(result_folder_path):
            os.makedirs(result_folder_path)


# cyclically determines the next result folder to be used
def get_next_result_folder(current_index, base_path=".", tmp_folder_name="tmp"):
    tmp_folder_path = os.path.join(base_path, tmp_folder_name)
    next_index = (current_index % 10) + 1
    next_result_folder_path = os.path.join(tmp_folder_path, f"result_{next_index}")

    # clean up the next result folder by removing its contents
    for filename in os.listdir(next_result_folder_path):
        file_path = os.path.join(next_result_folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    return next_result_folder_path


# remove temporary folder and its contents
def clean_up(base_path=".", tmp_folder_name="tmp"):
    tmp_folder_path = os.path.join(base_path, tmp_folder_name)
    if os.path.exists(tmp_folder_path):
        shutil.rmtree(tmp_folder_path)


# main funktion
def run():
    # define a list of directory names that represent specific tests
    directories = [
        "Serial",
        "Runs",
        "ApproximateEntropy",
        "BlockFrequency",
        "CumulativeSums",
        "DFT",
        "Frequency",
        "LinearComplexity",
        "LongestRun",
        "NonOverlappingTemplate",
        "RandomExcursions",
        "RandomExcursionsVariant",
        "Universal",
        "Rank",
        "OverlappingTemplate",
    ]

    config = load_config(
        "/home/jenny/Projekte/python/rng_evaluation/configuration/local.yaml"
    )
    directory_path = config["paths"]["testing_directory"]

    while True:
        # list all files in the directory
        files = os.listdir(directory_path)

        while files:
            # choice a random file from the list
            file_to_test = random.choice(files)

            # create directory for results
            results_directory = os.path.join(directory_path, "results")
            os.makedirs(results_directory, exist_ok=True)

            # path to results CSV file
            csv_file_path = os.path.join(results_directory, "results.csv")

            # create a list of binaryfiles in the directory
            binary_files = [
                os.path.join(directory_path, f)
                for f in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, f))
                and f.startswith("response")
            ]

            # Initialize the current index for the result folders
            current_index = 0

            create_tmp_and_result_folders()

            # run trough the list of binary files
            for binary_file in binary_files:
                path = get_next_result_folder(current_index)
                sts(binary_file, path)

                # write csv-file
                process_and_write_results(binary_file, directories, path, csv_file_path)

                # increment the current index with cyclization
                current_index = current_index + 1
                if current_index > 10:
                    current_index = 0

                # remove binary file after testing
                os.remove(binary_file)

            # remove the tested file from the list
            files.remove(file_to_test)

        # clean up temporary folders and files
        clean_up()

        print(
            "Processing completed. Press CTRL+C to exit the programm. To test more random numers, do nothing"
        )

        try:
            selected_time = 120
            print(
                f"The program waits {selected_time/60}  minute(s) and then check again for new random numbers to be tested."
            )
            time.sleep(selected_time)

        except KeyboardInterrupt:
            print("\n Program is terminated")
            sys.exit(0)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n Program is terminated")
        sys.exixt(0)
