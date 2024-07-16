import tkinter as tk
from tkinter import messagebox


class Tools:

    @staticmethod
    def binary_to_string(binary_data):
        return ''.join(format(byte, '08b') for byte in binary_data)

    @staticmethod
    def show_stars(stars):
        message = f"Star Rating: {stars}"

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Result", message)
