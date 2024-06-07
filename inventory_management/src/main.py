"""This is the main module."""

import tkinter as tk
from inventory_management.src.mainmenu import MainMenu
import os


def run_main() -> None:
    """
    Start the tkinter window.

    Args:
        None

    Returns:
        None

    """
    root = tk.Tk()
    width = 1200
    height = 700

    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen

    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2) - 50

    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.title("Inventory Management System")

    # logo_file_name_path = os.path.abspath(
    #     os.path.join(
    #         os.path.dirname(__file__),
    #         "images",
    #         "BusinessLogo.gif",
    #     )
    # )

    # img = tk.Image("photo", file=logo_file_name_path)
    # root.iconphoto(False, img)

    main_menu = MainMenu(root)
    main_menu.start()
