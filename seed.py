from sqlalchemy.orm import Session
from db import engine, Base, SessionLocal
from models import User
from utils import get_password_hash

def seed_data():
    db = SessionLocal()
    try:
        # Create admin user
        admin_user = User(
            username="admin1",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)

        # Create customer user
        customer_user = User(
            username="customer1",
            hashed_password=get_password_hash("customer123"),
            role="customer"
        )
        db.add(customer_user)

        db.commit()
        print("Data seeded successfully!")
    except Exception as e:
        print("Error seeding data:", str(e))
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    seed_data()
