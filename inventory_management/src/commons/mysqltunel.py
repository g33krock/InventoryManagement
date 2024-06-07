"""This module maintains and runs the ssh tunnel."""

import pandas as pd
import pymysql

# from sshtunnel import SSHTunnelForwarder


class MySqlTunel:
    """The SSH Tunel to connect and query the database through."""

    def __init__(self) -> None:
        """
        Initiallize the ssh tunnel and database connection.

        Args:
            None

        Returns:
            None

        """

        pd.set_option("display.max_columns", 500)
        pd.set_option("display.width", 1000)
        self.database_username = "root"
        self.database_password = "Cubby0619"
        self.localhost = "127.0.0.1"
        self.database_port = 3306
        self.database_name = "inventory_management"
        self.currentTable = ""

    # def open_ssh_tunnel(self):
    #     """
    #     Open an SSH tunnel and connect using a username and password.

    #     Args:
    #         None

    #     Returns:
    #         None

    #     """
    #     global tunnel
    #     tunnel = SSHTunnelForwarder(
    #         (self.ssh_host, 22),
    #         ssh_username=self.ssh_username,
    #         ssh_password=self.ssh_password,
    #         remote_bind_address=("127.0.0.1", 3306),
    #     )

    #     tunnel.start()

    def mysql_connect(self,) -> None:
        """
        Connect to a MySQL server using the SSH tunnel connection.

        Args:
            database_name(str):

        Returns:
            None

        """
        global connection

        connection = pymysql.connect(
            host=self.localhost,
            user=self.database_username,
            passwd=self.database_password,
            db=self.database_name,
            port=self.database_port,
        )

    def run_data(self, sql: str) -> None:
        """
        Run a given SQL query via the global database connection.

        Args:
            sql(str): Query to be executed.

        Returns:
            None

        """
        cursor = connection.cursor()
        cursor.execute(query=sql)
        connection.commit()

    def run_query(self, sql: str) -> pd.DataFrame:
        """
        Run a given SQL query via the global database connection.

        Args:
            sql(str): Query to be executed.

        Returns:
            pd.DataFrame: Result of the query.

        """
        return pd.read_sql_query(sql=sql, con=connection)

    def mysql_disconnect(self) -> None:
        """
        Close the MySQL database connection.

        Args:
            None

        Returns:
            None

        """
        connection.close()

    # def close_ssh_tunnel(self) -> None:
    #     """
    #     Close the SSH tunnel connection.

    #     Args:
    #         None

    #     Returns:
    #         None

    #     """
    #     tunnel.close
