# ================================
# Import necessary libraries for MongoDB connection
from pymongo import MongoClient
import mongoengine as me
import datetime  # We need this to parse dates for the MongoEngine schema

# ================================
# Define server connection parameters and connect to MongoDB using pymongo
SERVER_ADDRESS = "<your_server_address>"  # Add MongoDB server address here
PORT = "<port_number>"                    # Replace with MongoDB server port if different
USERNAME = "<username>"                   # Add MongoDB username here
PASSWORD = "<password>"                   # Add MongoDB password here

# Establish a connection to the MongoDB server with pymongo
try:
    connection = MongoClient(f'mongodb://{USERNAME}:{PASSWORD}@{SERVER_ADDRESS}:{PORT}')
    print("MongoDB connection established.")

    # List all databases on the server (for verification)
    db_names = connection.list_database_names()
    print("Available databases:", db_names)

# Handle connection errors
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# ================================
# Access a specific database and list collections

# Specify the target database and list its collections
try:
    db = connection['target_database']  # Replace 'target_database' with your database name
    collection_names = db.list_collection_names()
    print("Collections in 'target_database':", collection_names)

    # Access a specific collection (e.g., 'sample_collection')
    collection = db['sample_collection']  # Replace 'sample_collection' with your collection name
    # Retrieve and print the first document in the 'sample_collection' collection
    print("Sample document:", collection.find_one())

except Exception as e:
    print(f"Error accessing database or collection: {e}")

# ================================
# Define a MongoEngine Document schema for the sample collection

# Establish a connection to MongoDB with MongoEngine
try:
    me.connect('target_database', host=SERVER_ADDRESS, port=PORT, username=USERNAME, password=PASSWORD)

    # Define a general schema for a collection
    class SampleDocument(me.Document):
        field1 = me.StringField()                # Replace with actual field purpose
        field2 = me.StringField()                # Generalized field for string data
        field3 = me.IntField()                   # Generalized integer field
        field4 = me.StringField()                # Another generalized string field
        listField1 = me.ListField(me.StringField())  # Generalized list of strings
        listField2 = me.ListField(me.StringField())  # Another generalized list of strings
        timestamp = me.DateTimeField()           # Generalized timestamp field

    # Query to retrieve the first document in the 'SampleDocument' collection
    document = SampleDocument.objects().first()

    # Display retrieved document fields
    if document:
        print("Document details:")
        print("Field1:", document.field1)
        print("Field2:", document.field2)
        print("Field3:", document.field3)
        print("Field4:", document.field4)
        print("Timestamp:", document.timestamp)

# Handle connection and query errors
except Exception as e:
    print(f"Error with MongoEngine connection or schema definition: {e}")
