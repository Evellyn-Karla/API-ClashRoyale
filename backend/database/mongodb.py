from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

user_mongo = os.getenv('DB_USERNAME')
password_mongo = os.getenv('DB_PASSWORD')
database_name = os.getenv('DB_NAME')


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = f'mongodb+srv://{user_mongo}:{password_mongo}@cluster0.cek6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
        self.__database_name = database_name
        self.__client = None
        self.__db_connection = None

    def connectDB(self):
        self.__client = MongoClient(self.__connection_string, tls=True)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        return self.__db_connection
    
    
    def get_db_client(self):
        return self.__client
  















