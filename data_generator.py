import mysql.connector
from faker import Faker
import random

fake = Faker()

conn = mysql.connector.connect(
    host='localhost',
    user='root',  # Use your username here
    password='anandkhushi@2407',  # Use your password here
    database='skill_swap_db'
)

cursor = conn.cursor()

for i in range(50):  # Generate 50 unique users
    name = fake.name() + str(i)  # Append index to name for uniqueness
    skills = ', '.join(fake.words(random.randint(1, 5)))  # Random skills
    purpose = random.choice(['Collaboration', 'Learning', 'Networking'])  # Random purpose
    contact = fake.phone_number()  # Generate a random phone number
    profile_picture = fake.image_url()  # Generate a random image URL

    cursor.execute(
        "INSERT INTO users (name, skills, purpose, contact, profile_picture) VALUES (%s, %s, %s, %s, %s)",
        (name, skills, purpose, contact, profile_picture)
    )

conn.commit()
cursor.close()
conn.close()

print("Data generation complete!")
