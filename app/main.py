from fastapi import FastAPI
from app.config import settings
from app.routes import router
from database import SessionLocal, engine, Base
import uvicorn

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080, reload=True, workers=3)
