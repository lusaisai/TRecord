from trecord.database import Database
import pyodbc


class PyODBCMSSQL(Database):
    """This class implements the database using PyMySQL"""
    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        pass

    def get_data_type(self, type_code: int) -> str:
        pass

