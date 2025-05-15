import pandas as pd
from pymongo import MongoClient, errors

class MongoUploader:
    def __init__(self, db_name, collection_name):
        try:
            self.host="localhost"
            self.port=27017
            self.client = MongoClient(self.host,self.port)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except errors.ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")

    def conntest(self):
        try:
            print("Testing connection to MongoDB...")
            databases = self.client.list_database_names()
            print("Databases:", databases)
            collections = self.db.list_collection_names()
            print(f"Collections in '{self.db.name}':", collections)
            print("-------------")
        except Exception as e:
            print(f"Error listing databases or collections: {e}")

    def read_csv(self, csv_path):
        try:
            print(f"Reading CSV file from {csv_path}...")
            self.df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.df)} rows from CSV.")
            print("First 5 rows of the DataFrame:")
            print(self.df.head(5))
            print("--------------")
            return self.df.head(5).to_dict(orient='records')  # Return as list of dicts
        except FileNotFoundError:
            print(f"File not found: {csv_path}")
            return {"error": f"File not found: {csv_path}"}
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")
            return {"error": f"Error parsing CSV file: {e}"}


    def read_csv_mongo(self, csv_path):
        try:
            self.df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.df)} rows from CSV.")
            #print(self.df.head(5))
        except FileNotFoundError:
            print(f"File not found: {csv_path}")
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {e}")

    def upload_to_mongo(self):
        try:
            # Create unique index on sr_no
            print("Uploading...")
            self.df['sr_no'] = self.df['sr_no'].astype(int)
            self.collection.create_index("sr_no", unique=True)
            data_dict = self.df.to_dict(orient='records')
            result = self.collection.insert_many(data_dict)
            print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")
            print("--------------")
        except errors.BulkWriteError as bwe:
            print("Bulk write error occurred:")
            for error in bwe.details['writeErrors']:
                if error['code'] == 11000:  # Duplicate key error code
                    print(f"Duplicate key error: {error['errmsg']}")
                else:
                    print(error)
        except Exception as e:
            print(f"An error occurred during upload: {e}")
    def false_entry(self):
        try:
            print("Inserting false entry...")
            false_entry = {
                "sr_no": "ten",  
                "entity_name": 12345,  
                "category": 125,  
                "regulator": "RBI",  
                "fip_implementation_stage": {},  
                "fiu_implementation_stage": 98.6 
                }
            self.collection.insert_one(false_entry)
            print("False entry inserted.")
            print("--------------")
        except Exception as e:
            print(f"Error inserting false entry: {e}")

    def delete_all_documents(self):
        try:
            print("Deleting all documents from the collection...")
            result = self.collection.delete_many({})
            print(f"Deleted {result.deleted_count} documents from the collection.")
            print("--------------")
        except Exception as e:
            print(f"Error deleting documents: {e}")

    def read_db(self, limit):
        docs_list = []
        try:
            print(f"Reading first {limit} documents from the collection...")
            cursor = self.collection.find().limit(limit)
            flag = 0
            for doc in cursor:
                doc['_id'] = str(doc['_id'])  # Convert ObjectId to string for JSON serialization
                print(doc)
                docs_list.append(doc)
                flag = 1
            if flag == 0:
                print("No documents found.")
            print("--------------")
            return docs_list
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []

