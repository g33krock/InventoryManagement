"""Module contains default frame creation code."""

import tkinter as tk
from tkinter import END
from tkinter.scrolledtext import ScrolledText


class BaseFrame:
    """Class contains code to generate the default frame."""

    def __init__(self, parent: tk.Frame, back_command) -> None:
        self.back_command = back_command
        self.mainframe = tk.Frame(parent)
        self.mainframe.grid()
        self.database = "inventory_management"

    def print_to_gui(self, textbox: ScrolledText, message: str) -> None:
        """
        Print provided text to selected textbox.

        Args:
            textbox (ScrolledText): Text field for text to be displayed.
            message (str): Text to be displayed.

        Returns:
            None

        """
        textbox.config(state="normal")
        textbox.delete("1.0", END)
        textbox.insert(END, message + "\n")
        self.mainframe.update_idletasks()
        textbox.config(state="disabled")

    def destroy(self) -> None:
        self.mainframe.destroy()

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_last_widget(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"
