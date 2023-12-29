import pymongo
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, db_name, collection_name):
        # Connect to the MongoDB server
        self.client = MongoClient("mongodb://localhost:27017/")  # Change connection string as needed

        # Access the specified database and collection
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_user(self, user_data):
        # Insert a new user into the collection
        self.collection.insert_one(user_data)

    def find_user_by_uid(self, uid):
        # Find a user by UID
        result = self.collection.find_one({"uid": uid})
        return result

    def create_new_user(self, name, age, uid):
        # Create a new user and insert into the collection
        new_user = {
            "user": name,
            "uid": uid,
            "age": age,
            "requested_flights": [],
            "past_flights": []
        }
        self.insert_user(new_user)

    # Method to insert a user into the "past_flights" array
    def add_to_past_flights(self, uid, past_flight_obj):
        # Find the user by UID
        user = self.collection.find_one({"uid": uid})

        # Append the past flight object to "past_flights"
        user["past_flights"].append(past_flight_obj)

        # Update the user in the collection
        self.collection.update_one({"uid": uid}, {"$set": user})

    # Method to insert a requested flight object into "requested_flights"
    def add_to_requested_flights(self, uid, requested_flight_obj):
        # Find the user by UID
        user = self.collection.find_one({"uid": uid})

        # Append the requested flight object to "requested_flights"
        user["requested_flights"].append(requested_flight_obj)

        # Update the user in the collection
        self.collection.update_one({"uid": uid}, {"$set": user})

    # Function to search a specific requested flight by payment ID
    def search_requested_flight_by_payment_id(self, payment_id):
        # Search for the requested flight with the given payment ID
        result = self.collection.find_one({"requested_flights.payment.id": payment_id})
        return result

# Example usage:
mongo_handler = MongoDBHandler(db_name="test", collection_name="user_data")

# Example: Find a user by UID
uid_to_find = "2312421412412"
found_user = mongo_handler.find_user_by_uid(uid_to_find)
print("Found User:")
print(found_user)

# Example: Create a new user
new_name = "John Doe"
new_age = 25
new_uid = "987654321"
mongo_handler.create_new_user(new_name, new_age, new_uid)
print(f"User {new_name} created.")

# Verify that the new user is in the collection
found_new_user = mongo_handler.find_user_by_uid(new_uid)
print("Found New User:")
print(found_new_user)

# Example: Add a past flight to a user
uid_to_update = "2312421412412"
past_flight_data = {
    "booking_detials": {
        "TraceId": "YYY",
        "ResultIndex": "YYYY",
        "Passengers": [
            # ... passenger details ...
        ]
    },
    "payment_details": {
        "PaymentType": "CreditCard"
    }
}
mongo_handler.add_to_past_flights(uid_to_update, past_flight_data)

# Example: Add a requested flight to a user
requested_flight_data = {
    "details": {
        "ChildCount": "0",
        "InfantCount": "0",
        "JourneyType": "1",
        "Segments": [
            # ... flight segment details ...
        ]
    },
    "payment": {
        "status": "pending",
        "id": "12345"
    }
}
mongo_handler.add_to_requested_flights(uid_to_update, requested_flight_data)

# Example: Search for a requested flight by payment ID
payment_id_to_search = "12345"
found_requested_flight = mongo_handler.search_requested_flight_by_payment_id(payment_id_to_search)
print("Found Requested Flight:")
print(found_requested_flight)


