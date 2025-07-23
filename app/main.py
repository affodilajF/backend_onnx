from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import video_router

app = FastAPI(title="FastAPI Video AI Stream")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sesuaikan dengan frontend kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router.router)
