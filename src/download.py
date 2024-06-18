#!/usr/bin/env python

import os
import tkinter as tk
from tkinter import filedialog

import requests


# Funktion zur Auswahl eines Verzeichnisses mittels einer grafischen Benutzeroberfläche
def select_directory():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


def download_random_numbers(directory_path, num_files=2):
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


def main():
    directory_path = select_directory()

    # Herunterladen der Zufallszahlen in das ausgewählte Verzeichnis
    download_random_numbers(directory_path)


if __name__ == "__main__":
    main()
