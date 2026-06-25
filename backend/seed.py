import random
from faker import Faker
from database import SessionLocal, engine
import models

fake = Faker()
random.seed(42)

CATEGORIES = ["books", "electronics", "clothing", "sports", "home"]

def seed():
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(models.Product).count() > 0:
            print("product already exists")
            return
        #products
        for i in range(1,101):
            db.add(models.Product(
                name=fake.catch_phrase(),
                category=random.choice(CATEGORIES),
                price=round(random.uniform(5.99,299.99),2),
                stock=random.randint(0,500),
                description=fake.sentence(nb_words=10),
                rating=round(random.uniform(1.0,5.0),1)
            ))
        #users
        for i in range(1,21):
            db.add(models.User(
                name=fake.name(),
                email=fake.unique.email(),
                address=fake.address().replace("\n",", "),
                phone=fake.phone_number(),
            ))

        db.commit()
        print("Creates 100 products and 20 users")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
