from fastapi import FastAPI, Request
from fastapi_jwt_auth import AuthJWT
from app.config import settings
from app.auth import auth_router
from app.routes import router
from app.database import engine, Base
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
import logging


Base.metadata.create_all(bind=engine)
app = FastAPI()
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

app.include_router(auth_router)
app.include_router(router)

@AuthJWT.load_config
def get_config():
    return settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080, reload=True, workers=3)
