#file to generate a large number of profile data using Faker Python library
import random
from faker import Faker
from service import profile_collection, hash_password

#library with built in datasets containing real-world values and functions to select from relevant datasets
fake = Faker()

#opitions for selections
genders = ["male", "female", "nonbinary", "transgender", "other"]
politics = ["conservative", "moderate", "liberal", "not", "other"]
religions = ["agnostic", "atheist", "buddhist", "catholic", "christian", "hindu", "jewish", "muslim", "spiritual", "other", "not"]
children = ["want", "open", "unsure", "dont", "not"]
have_children = ["yes", "no", "not"]

#Function to generate profiles with random data. Use Faker for generation and random for random selection from options
def generate_profile_data():
    return{
        "username": fake.user_name(),
        "password": hash_password("Robert88"), #use same password for all users for ease of testing
        "email": fake.email(),
        "first": fake.first_name(),
        "last": fake.last_name(),
        "age": random.randint(18, 65), #random age between 18 and 65
        "occupation": fake.job(),
        "gender": random.choice(genders),
        "matchPreferences": random.sample(genders, k=random.randint(1, 3)), #randomly select how many genders user wants to match with
        "politics": random.choice(politics),
        "religion": random.choice(religions),
        "wantChildren": random.choice(children),
        "haveChildren": random.choice(have_children),
    }

#instert 50 generated profiles into Mongo db
for _ in range(50):
    profile_collection.insert_one(generate_profile_data())

print("Sample profiles added.") #confirm function ran