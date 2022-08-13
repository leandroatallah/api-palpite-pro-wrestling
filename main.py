from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import model
from config import engine
import router

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://dashboard-palpite-pro-wrestling.vercel.app",
    "https://dashboard-palpite-pro-wrestling.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.router.get('/')
def home():
    return {"Welcome Home"}


app.include_router(router.router, prefix="/event", tags=["event"])
