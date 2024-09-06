from fastapi import FastAPI
from api.endpoints import router as api_router
from api.models import Base, engine  # Import Base and engine

# Create all tables
Base.metadata.create_all(bind=engine)  # Ensure all tables are created

# Initialize FastAPI app
app = FastAPI()

# Include the API routes
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


