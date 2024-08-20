#!/usr/bin/env python
import os
import requests
import file_counter
from helper import load_config


def download_random_numbers(directory_path):
    os.chdir(directory_path)
    print("Downloading random numbers")

    url = "http://localhost"
    i = file_counter.increment()
    file_name = f"response{i}.bin"

    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print(f"File {file_name} downloaded successfully.")
        else:
            print(f"Failed to download file {i}. Status code: {response.status_code}")


def main():
    config = load_config("~/Projekte/python/rng_evaluation/configuration/local.yaml")
    directory_path = config["paths"]["download_directory"]
    download_random_numbers(directory_path)


if __name__ == "__main__":
    main()
