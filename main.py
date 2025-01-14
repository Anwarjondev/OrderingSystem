from fastapi import FastAPI
from db import engine, Base
from routers.admin import admin_router
from routers.customer import customer_router
from routers.auth import auth_router

# Initialize the FastAPI application
app = FastAPI()

# Include the authentication router
app.include_router(auth_router)

# Create the database tables if they don't already exist
Base.metadata.create_all(bind=engine)

# Include the admin and customer routers
app.include_router(admin_router)
app.include_router(customer_router)
