"""This is the mainmenu moduel."""

import tkinter as tk
from tkinter import Button

from inventory_management.src.frames import (
    AddUserFrame,
)


class MainMenu:
    """Create and display a main menu frame."""

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize method of the MainMenu class.

        Args:
            root (tk.Tk): This is the root GUI window.

        Returns:
            None

        """
        self.root = root
        self.frame_container = tk.Frame(self.root)
        self.frame_container.pack()

        self.add_user_button = Button(
            self.frame_container,
            text="Add User",
            height=1,
            width=20,
            command=lambda: self.show_frame("adduser"),
        )

        self.set_grid()

        self.current_frame = None
        self.current_frame_type = "mainmenu"

    def show_frame(self, frame_name: str) -> None:
        """
        Destroy MainMenu frame and creates new frame.

        Args:
            frame_name (str): Name of the frame to be created.

        Returns:
            None

        """
        if self.current_frame_type != "mainmenu":
            if self.current_frame is not None:
                self.current_frame.destroy()
            self.current_frame_type = "mainmenu"
        else:
            self.current_frame_type = frame_name

        self.add_user_button.grid_forget()

        back_to_menu = self.back_to_menu

        frame_dict = {
            "adduser": AddUserFrame,
        }

        frame_class = frame_dict[frame_name]
        self.current_frame = frame_class(
            parent=self.frame_container,
            back_command=back_to_menu,
        )

    def set_grid(self) -> None:
        self.add_user_button.grid(row=0, column=0, columnspan=1, padx=10, pady=5)

    def back_to_menu(self) -> None:
        """
        Destroy current frame and regenerates the menu frame.

        Args:
            None

        Returns:
            None

        """
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Show the main menu buttons again
        self.add_user_button.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
        self.current_frame_type = "mainmenu"

    def start(self) -> None:
        """
        Start the frame loop.

        Args:
            None

        Returns:
            None

        """
        self.root.mainloop()
