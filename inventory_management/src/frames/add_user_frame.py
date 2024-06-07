"""Module for NewPrint Frame."""

import tkinter as tk
from tkinter import Label, ttk, Text, Button
from tkinter import messagebox
import pandas as pd
from inventory_management.src.commons.mysqltunel import MySqlTunel
from inventory_management.src.frames.baseframe import BaseFrame
import inventory_management.src.logic.add_user


class AddUserFrame(BaseFrame):
    """Code to create and run AddUserFrame."""

    def __init__(self, parent: tk.Frame, back_command) -> None:
        super(AddUserFrame, self).__init__(parent, back_command)

        self.role_dict = {}
        self.role_var = tk.StringVar()

        # Create Objects
        self.first_name_label = Label(
            self.mainframe,
            text="First Name:",
            width=20,
        )
        self.first_name = Text(
            self.mainframe,
            height=1,
            width=20,
        )
        self.last_name_label = Label(
            self.mainframe,
            text="Last Name:",
            width=20,
        )
        self.last_name = Text(
            self.mainframe,
            height=1,
            width=20,
        )
        self.email_label = Label(
            self.mainframe,
            text="Email:",
            width=20,
        )
        self.email = Text(
            self.mainframe,
            height=1,
            width=20,
        )
        self.role_label = Label(
            self.mainframe,
            text="Role:",
            width=20,
        )
        self.role_combobox = ttk.Combobox(
            self.mainframe,
            width=20,
            justify="center",
            textvariable=self.role_var,
            state="read-only",
        )
        self.submit_button = Button(
            self.mainframe,
            text="Submit",
            command=self.submit,
        )
        self.cancel_button = Button(
            self.mainframe,
            text="Cancel",
            command=self.back_command,
        )

        # Combobox Values and Config
        self.get_roles_list()
        self.role_combobox["values"] = list(self.role_dict.keys())

        # Set Grid
        self.first_name_label.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew",
        )
        self.first_name.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
            columnspan=2,
        )
        self.last_name_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="ew",
        )
        self.last_name.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
            columnspan=2,
        )
        self.email_label.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="ew",
        )
        self.email.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
            columnspan=2,
        )
        self.role_label.grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="ew",
        )
        self.role_combobox.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
            columnspan=2,
        )
        self.submit_button.grid(
            row=7,
            column=0,
            padx=5,
            pady=5,
            sticky="ew",
        )
        self.cancel_button.grid(
            row=7,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
            columnspan=2,
        )

    def get_roles_list(self) -> None:
        """
        Fetch the roles list from the database.

        Args:
            None

        Returns:
            None

        """
        tunel = MySqlTunel()
        tunel.mysql_connect()
        query = "select * from roles"
        data = tunel.run_query(query)
        tunel.mysql_disconnect()
        df = pd.DataFrame(data=data)
        for index in df.index:
            self.role_dict[df["role"][index]] = df["id"][index]

    def submit(self) -> None:
        """
        Submit the new user to the database.

        Args:
            None

        Returns:
            None

        """
        pass
