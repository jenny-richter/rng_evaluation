#!/usr/bin/env python

import csv
import os
import random
import shutil
import statistics
import subprocess
import tkinter as tk
from tkinter import filedialog

from tools import Tools as tools


# Funktion zur Auswahl eines Verzeichnisses mittels einer grafischen Benutzeroberfläche
def select_directory():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()


def sts(file_path, dir):
    verbose_level = 1
    instance = 1
    work_dir = dir
    file_format = "r"
    mode = "b"

    change_Parameters = "1=20000,2=10,3=9,4=8,5=16,6=1000,7=1073,9=1000000"

    command = [
        "/home/jenny/Projekte/rating_system/testing/sts/sts_legacy_fft",
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

    # Debugging-Informationen
    print("Aktuelles Arbeitsverzeichnis:", os.getcwd())
    full_command_path = os.path.abspath(command[0])
    print("Vollständiger Pfad zu sts_legacy_fft:", full_command_path)

    if not os.path.exists(full_command_path):
        print(f"Ausführbare Datei nicht gefunden: {full_command_path}")
        return

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des Befehls: {e}")
    except FileNotFoundError as e:
        print(f"Datei nicht gefunden Fehler: {e}")


# Funktion zur Berechnung des Durchschnitts der Ergebnisse aus mehreren Verzeichnissen
def calculate_average_of_results(directories, path):
    res = []
    base_path = path
    for dir in directories:
        result_path = os.path.join(base_path, dir, "results.txt")
        res.append(calculate_avg_of_results_txt(result_path, str(dir)))
    return statistics.fmean(res)


# Zählt die Anzahl von 'success' und 'failure' in stats.txt Dateien über mehrere Verzeichnisse
def count_Success_Failure(directories, path):
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


# Berechnet den Durchschnitt der numerischen Werte in einer results.txt Datei und ignoriert ungültige Zeilen
def calculate_avg_of_results_txt(path, dir):
    numbers = []
    with open(path, "r") as file:
        for line in file:
            cleaned_line = line.strip()
            if cleaned_line.upper() != "__INVALID__":
                try:
                    number = float(cleaned_line)
                    numbers.append(number)
                except ValueError:
                    continue
    if numbers:
        avg = statistics.fmean(numbers)
        print(f"{dir} : {avg}")
        return avg
    else:
        return 0.0


# Funktion zur Erstellung eines temporären Ordners und Ergebnis-Unterordner darin
def create_tmp_and_result_folders(base_path=".", tmp_folder_name="tmp"):
    tmp_folder_path = os.path.join(base_path, tmp_folder_name)
    if not os.path.exists(tmp_folder_path):
        os.makedirs(tmp_folder_path)
    for i in range(1, 11):
        result_folder_path = os.path.join(tmp_folder_path, f"result_{i}")
        if not os.path.exists(result_folder_path):
            os.makedirs(result_folder_path)


# Bestimmt den nächsten Ergebnisordner, der verwendet werden soll, zyklisch durch eine Menge von Ordnern
def get_next_result_folder(current_index, base_path=".", tmp_folder_name="tmp"):
    tmp_folder_path = os.path.join(base_path, tmp_folder_name)
    next_index = (current_index % 10) + 1
    next_result_folder_path = os.path.join(tmp_folder_path, f"result_{next_index}")

    # Bereinigen des nächsten Ergebnisordners, indem dessen Inhalt entfernt wird
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


# Schreibt die Analyseergebnisse in eine CSV-Datei, einschließlich Erfolg/Misserfolg Zählungen, Verhältnis, durchschnittlicher p-Wert
def write_in_to_csv_file(
    file_path, overall_avg_pvalue, csv_file_path, file_exists, success, failure
):
    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                [
                    "Filename",
                    "Average P-Value",
                    "Stars",
                    "File Size (MB)",
                    "Testsuite",
                    "Success",
                    "Failure",
                    "Ratio",
                ]
            )

    ratio = success / failure if failure != 0 else "undefined"
    stars = tools.get_stars(overall_avg_pvalue)
    filename = os.path.basename(file_path)
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024**2)

    with open(csv_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                filename,
                overall_avg_pvalue,
                stars,
                round(file_size_mb, 2),
                "FullNist-C",
                success,
                failure,
                ratio,
            ]
        )
    print(
        f"For File: {filename}, Overall Average P-Value: {overall_avg_pvalue}, File Size: {round(file_size_mb, 2)} MB"
    )


# Entfernt den temporären Ordner und dessen Inhalte
def clean_up(base_path=".", tmp_folder_name="tmp"):
    tmp_folder_path = os.path.join(base_path, tmp_folder_name)
    if os.path.exists(tmp_folder_path):
        shutil.rmtree(tmp_folder_path)


# Hauptfunktion zur Orchestrierung des Analyseprozesses
def run():
    # Definieren einer Liste von Verzeichnisnamen, die spezifische Tests darstellen
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

    # Aufruf der Funktion zur Auswahl eines Verzeichnisses durch den Benutzer
    directory_path = select_directory()

    # Liste aller Dateien im ausgewählten Verzeichnis
    files = os.listdir(directory_path)

    # Solange wie Dateien im Verzeichnis sind:
    while files:
        # Wahl einer zufälligen Datei aus der Liste
        file_to_test = random.choice(files)

        # Verzeichnis für die Ergebnisse erstellen
        results_directory = os.path.join(directory_path, "results")
        os.makedirs(results_directory, exist_ok=True)

        # Pfad zur CSV-Datei, in der die Ergebnisse gespeichert werden
        csv_file_path = os.path.join(
            results_directory, "results.csv"
        )  # setzt Pfad zusammen
        file_exists = os.path.isfile(
            csv_file_path
        )  # Übrprüft ob Datei an angebeenem Pfad existiert

        # Erstellen einer Liste der Binärdateien im Verzeichnis
        binary_files = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
            and f.startswith("response")
        ]

        # Initialisieren des aktuellen Index für die Ergebnisordner
        current_index = 0

        # Erstellen temporärer und Ergebnisordner
        create_tmp_and_result_folders()

        # Durchlaufen der Liste der Binärdateien
        for binary_file in binary_files:
            # Bestimmen des nächsten Ergebnisordners
            path = get_next_result_folder(current_index)

            # Ausführen der statistischen Tests
            sts(binary_file, path)

            # Berechnen des Durchschnitts der Ergebnisse
            avg = calculate_average_of_results(directories, path)

            # Zählen der Erfolgs- und Fehlermeldungen
            success, failure = count_Success_Failure(directories, path)

            # Ausgabe der Ergebnisse
            print("All : ", avg)
            print("Success: ", success, " Failure: ", failure)

            # Schreiben der Ergebnisse in die CSV-Datei
            write_in_to_csv_file(
                binary_file, avg, csv_file_path, file_exists, success, failure
            )

            # Erhöhen des aktuellen Indexes, mit Zyklisierung
            current_index = current_index + 1
            if current_index > 10:
                current_index = 0

            # Löschen der Binärdatei nach dem Test
            os.remove(binary_file)

        # Entfernen der getesteten Datei aus der Liste
        files.remove(file_to_test)

    # Aufräumen der temporären Ordner und Dateien
    clean_up()


if __name__ == "__main__":
    run()
