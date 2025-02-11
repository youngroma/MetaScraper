from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from app.config import settings
from app.auth import auth_router
from app.routes import router
from app.database import SessionLocal, engine, Base
import uvicorn

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router)
app.include_router(router)

@AuthJWT.load_config
def get_config():
    return settings


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080, reload=True, workers=3)
