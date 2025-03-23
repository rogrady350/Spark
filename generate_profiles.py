#file to generate a large number of profile data using Faker Python library
import random
from faker import Faker
from service import profile_collection

fake = Faker()

#function to generate profiles with random data
def generate_profile_data():
    

    return{}

#instert 50 generated profiles into Mongo db
for _ in range(50):
    profile_collection.insert_one(generate_profile_data())

print("Sample profiles added.")