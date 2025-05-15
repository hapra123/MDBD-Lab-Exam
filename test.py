from engine import MongoUploader

DATABASE_NAME = "bankdata"
COLLECTION_NAME = "bankinfo"
CSV_FILE_PATH = "bankdata.csv"

engine = MongoUploader(DATABASE_NAME, COLLECTION_NAME)
engine.read_csv(CSV_FILE_PATH)
engine.conntest()
engine.read_db(limit=2)  
engine.delete_all_documents()
engine.read_db(limit=2)  
engine.upload_to_mongo()
engine.read_db(limit=2) 
engine.upload_to_mongo()
engine.false_entry()

#engine.