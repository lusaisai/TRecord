from trecord.database import Database
from trecord.error import TRecordError
import pymysql


class PyMySQL(Database):
    """This class implements the database using PyMySQL"""
    def __init__(self) -> None:
        super().__init__()

    def connect(self, database_url: str):
        super().connect(database_url)
        self.connection = pymysql.connect(host=self.database_url.host,
                                          user=self.database_url.username,
                                          password=self.database_url.password,
                                          db=self.database_url.database,
                                          charset='utf8mb4')

    def query(self, query: str, limit: int = None):
        try:
            result = super().query(query, limit)
            return result
        except pymysql.MySQLError as err:
            raise TRecordError(err)

    def get_data_type(self, type_code: int) -> str:
        """
        Check the type code and return a string description
        :param type_code:
        :return:
        """
        mapping = {
            pymysql.STRING: 'STRING',
            pymysql.BINARY: 'BINARY',
            pymysql.NUMBER: 'NUMBER',
            pymysql.DATE: 'DATE',
            pymysql.TIME: 'TIME',
            pymysql.TIMESTAMP: 'TIMESTAMP',
            pymysql.ROWID: 'ROWID'
        }
        for key in mapping.keys():
            if type_code == key:
                return mapping[key]

    def get_version(self):
        return self.read('select version()')[1][0]

    def get_current_db(self):
        return self.read('select database()')[1][0]


if __name__ == '__main__':
    sql = PyMySQL()
    sql.connect('mysql+pymysql://lusaisai:lusaisai@198.58.115.91/employees')
    print(sql.get_version())
    print(sql.get_current_db())
    print(sql.query('show tablesaa;'))
    print(sql.query('select version();'))
    print(sql.query('select * from departments;', 5))
    print(sql.query('select * from employees;', 20))
