from pymongo import MongoClient
from ..configs.mongodb_configs import mongodb_infos

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = 'mongodb+srv://{}:{}@cluster0.cek6z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'.format(mongodb_infos['USERNAME'],
        mongodb_infos['PASSWORD'])



        self.__database_name = mongodb_infos['DB_NAME']
        self.__client = None
        self.__db_connection = None

    def connectDB(self):
        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__database_name]

    def get_db_connection(self):
        return self.__db_connection
    
    
    def get_db_client(self):
        return self.__client
  















