import tkinter as tk
from tkinter import filedialog
import yaml


# Funktion zur Auswahl eines Verzeichnisses mittels einer grafischen Benutzeroberfläche
def select_directory():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory()

def load_config(config_path):
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)