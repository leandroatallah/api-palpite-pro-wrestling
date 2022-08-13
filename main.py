from fastapi import FastAPI
import model
from config import engine
import router

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.router.get('/')
def home():
    return {"Welcome Home"}


app.include_router(router.router, prefix="/event", tags=["event"])
