"""Script for uploading the cleaned data to the RDS."""

from os import environ as ENV, _Environ

from dotenv import load_dotenv
from mssql_python import connect, Connection


def get_db_connection(config: _Environ) -> Connection:
    """Returns a connection the SQL Server database."""

    return connect(
        f"Server={config["SERVER_NAME"]};Database=" + "{" + config["DB_NAME"] + "}" +
        ";Encrypt=yes;TrustServerCertificate=no;Authentication=ActiveDirectoryInteractive"
    )


if __name__ == "__main__":

    load_dotenv()
