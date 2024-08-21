# RNG-Evaluierungsprojekt

Dieses Projekt dient der kontinuierlichen Evaluierung von Zufallszahlengeneratoren (RNG) mithilfe statistischer Tests.

## Projektübersicht

Das Projekt besteht aus mehreren Python-Skripten, die zusammenarbeiten, um Zufallszahlen herunterzuladen, zu analysieren und die Ergebnisse zu verarbeiten.

### Hauptkomponenten:

1. `download.py`: Lädt Zufallszahlen von einem spezifizierten Server herunter.
2. `evaluation.py`: Führt statistische Tests auf den heruntergeladenen Daten durch.
3. `csv_writer_nist_results.py`: Verarbeitet die Testergebnisse und schreibt sie in eine CSV-Datei.
4. `file_counter.py`: Verwaltet einen Zähler für die heruntergeladenen Dateien.
5. `helper.py`: Enthält Hilfsfunktionen, wie das Laden von Konfigurationsdateien.
6. `tools.py`: Bietet zusätzliche Werkzeuge für die Datenverarbeitung.

## Installation

1. Klonen Sie das Repository:
   ```
   git clone https://github.com/jenny-richter/rng_evaluation
   ```

2. Installieren Sie die erforderlichen Abhängigkeiten:
   ```
   cd [Projektverzeichnis]
   pipenv install
   ```

## Konfiguration

1. Passen Sie die Datei `configuration/local.yaml` an Ihre lokale Umgebung an.
2. Stellen Sie sicher, dass die Pfade in der Konfigurationsdatei korrekt sind, insbesondere:
   - `download_directory`: Verzeichnis für heruntergeladene Zufallszahlen
   - `testing_directory`: Verzeichnis für die Durchführung der Tests
   - `sts_legacy_fft_directory`: Pfad zum STS (Statistical Test Suite) Programm

## Verwendung

1. Starten Sie den Download-Prozess durch Instalation eines Cronjobs:

2. Führen Sie die Evaluierung durch:
   ```
   ./src/evaluation.py
   ```
3. Die Ergebnisse werden in einer CSV-Datei im `results`-Verzeichnis gespeichert.


## Hinweise

- Das Programm läuft kontinuierlich und prüft regelmäßig auf neue Zufallszahlen zum Testen.
- Um das Programm zu beenden, drücken Sie Strg+C und entfernen Sie den Cronjob.
- Stellen Sie sicher, dass genügend Speicherplatz für die heruntergeladenen Daten und Testergebnisse vorhanden ist.
