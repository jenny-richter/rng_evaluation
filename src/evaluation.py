#!/usr/bin/env python3
import os
import shutil
import subprocess
import random
import sys
import time
from csv_writer_nist_results import process_and_write_results
from helper import select_directory, load_config

# from csv_writer_nist_results import count_Success_Failure

# Funktion zur Ausführung eines Befehls zur statistischen Analyse
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

    while True:
        # Liste aller Dateien im ausgewählten Verzeichnis
        files = os.listdir(directory_path)

        # Solange wie Dateien im Verzeichnis sind:
        while files:
            # Wahl einer zufälligen Datei aus der Liste
            file_to_test = random.choice(files)
            # file_path = os.path.join(directory_path, file_to_test)

            # Verzeichnis für die Ergebnisse erstellen
            results_directory = os.path.join(directory_path, "results")
            os.makedirs(results_directory, exist_ok=True)

            # Pfad zur CSV-Datei, in der die Ergebnisse gespeichert werden
            csv_file_path = os.path.join(
                results_directory, "results.csv"
            )  # setzt Pfad zusammen

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

                # _,failure= count_Success_Failure(directories, path)

                # if (failure>=1):
                #     sts(binary_file,path)
                #     print("Zufallszahlen werden ein 2.mal getestet")

                process_and_write_results(binary_file, directories, path, csv_file_path)

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

        print(
            "Verarbeitung abgeschlossen drücke Str+C um das Programm zu beenden, um noch weitere Zufallszahlen zu testen mache nichts"
        )
        try:
            print(
                "Das Programm wartet 1 Minute und schaut dann nochmal nach neuen zu tetstenden Zufallszahlen"
            )
            time.sleep(60)

        except KeyboardInterrupt:
            print("\n Programm wird beendet...")
            sys.exit(0)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n Programm wird beendet")
        sys.exixt(0)
