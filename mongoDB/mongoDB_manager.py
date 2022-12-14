import pymongo

class MongoDBManager:                   # Singleton 클래스
    __instance = None                   # 언더바 _를 두개 붙히면 private
    client = pymongo.MongoClient(host="localhost", port = 27017)        # 서버 접속정보
    database = None                                  # DB 이름, 콜렉션 이름 

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = object.__new__(cls, *args, **kwargs)

        return cls.__instance

    def get_data(cls, query, collection_name):
        # print(str(cls.database is not None))
        # assert cls.database
        
        cls.database = cls.client["SmartHomeService"][collection_name]
        if(cls.database is not None):
            return cls.database.find(query)
    
    def add_data(cls, data, collection_name):
        
        cls.database = cls.client["SmartHomeService"][collection_name]

        if(type(data) is list):
            return cls.database.insert_many(data)

        else:
            return cls.database.insert_one(data)