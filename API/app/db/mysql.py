from datetime import timedelta
from mysql.connector import pooling
from utils import Config


class SQLProvider:
    def __init__(self):
        db_config = Config().get("database")
        if db_config == None:
            raise Exception("Dữ liệu cấu hình hệ thống không tồn tại")

        self.config = {
            "user": db_config["user"],
            "password": db_config["password"],
            "host": db_config["host"],
            "port": db_config["port"],
            "database": db_config["name"],
            "ssl_verify_cert": db_config["ssl_verify_cert"],
        }
        self.connection_pool = pooling.MySQLConnectionPool(
            pool_name="mypool", pool_size=5, **self.config
        )

    def get_connection(self):
        return self.connection_pool.get_connection()

    def execute_query(self, query: str, params: tuple = ()):
        """
        Thực thi truy vấn SELECT.
        """
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        finally:
            if cursor:
                cursor.close()
            connection.close()

    def execute_update(self, query: str, params: tuple = ()):
        """
        Thực thi truy vấn INSERT/UPDATE/DELETE.
        """
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount
        finally:
            if cursor:
                cursor.close()
            connection.close()
