from fastapi import FastAPI
from app.routes.user import router as user_router
from app.core.database import Base
from app.core.database import engine

from app.models.user import User
from app.models.checkin import Checkin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GymFlow API",
    version="1.0.0"
)

app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "GymFlow API funcionando!"
    }

for route in app.routes:
    print(route.path)