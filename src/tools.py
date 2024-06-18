import random
import tkinter as tk
from tkinter import filedialog, messagebox


class Tools:

    @staticmethod
    def get_stars(avg_pvalue):
        return {
            avg_pvalue <= 0.1: "1 Star",
            0.1 < avg_pvalue <= 0.3: "2 Stars",
            0.3 < avg_pvalue <= 0.5: "3 Stars",
            0.5 < avg_pvalue <= 0.7: "4 Stars",
            avg_pvalue > 0.7: "5 Stars",
        }.get(True, "Invalid avg_pvalue")

    @staticmethod
    def binary_to_string(binary_data):
        return ''.join(format(byte, '08b') for byte in binary_data)

    @staticmethod
    def show_stars(stars):
        message = f"Star Rating: {stars}"

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Result", message)
