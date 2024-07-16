#!/usr/bin/env python

import os
import requests
import file_counter
from helper import load_config

def download_random_numbers(directory_path):
    os.chdir(directory_path)

    for i in range(num_files):
        response = requests.get("http://localhost")
        if response.status_code == 200:
            file_name = f"response{i}.bin"  # Generiere den Dateinamen
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"File {file_name} downloaded successfully.")
        else:
            print(f"Failed to download file {i}. Status code: {response.status_code}")
    response = requests.get("http://localhost")
    i = file_counter.increment()
    if response.status_code == 200:
        file_name = f"response{i}.bin"  # generate file name
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"File {file_name} downloaded successfully.")
    else:
        print(f"Failed to download file {i}. Status code: {response.status_code}")


def main():
    config = load_config("~/Projekte/python/rng_evaluation/configuration/local.yaml")

    directory_path = config["paths"]["download_directory"]
    # Herunterladen der Zufallszahlen in das ausgewählte Verzeichnis
    download_random_numbers(directory_path)


if __name__ == "__main__":
    main()
