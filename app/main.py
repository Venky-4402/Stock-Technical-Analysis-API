# Import FastAPI framework
from fastapi import FastAPI
#Importing required instances from modules created
from app.api import indicators
from app.auth.auth import router as auth_router
# Initialize the FastAPI application with a custom title
app = FastAPI(title="Kalpi Technical Indicators API")
# Include the authentication routes 
app.include_router(auth_router)
# Include the technical indicators API routes
app.include_router(indicators.router)
