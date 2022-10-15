from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import model
from config import engine
from api.event import routes as event_routes
from api.user import routes as user_routes

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


app.include_router(user_routes.router, prefix="/user", tags=["user"])
app.include_router(event_routes.router, prefix="/event", tags=["event"])
