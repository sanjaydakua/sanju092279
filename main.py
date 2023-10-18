# main.py
from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app.models import Base  # Import your Base from the models

# Create the tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)