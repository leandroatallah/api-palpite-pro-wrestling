from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import model
from config import engine
import router_user
import router_event

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
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


app.include_router(router_user.router, prefix="/user", tags=["user"])
app.include_router(router_event.router, prefix="/event", tags=["event"])
