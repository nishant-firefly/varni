from fastapi import FastAPI
from api import endpoints

app = FastAPI()

# Include API routes
app.include_router(endpoints.router)
