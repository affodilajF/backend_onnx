# main.py
import multiprocessing as mp
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.routes_ws import router as ws_router
from app.routers.routes_api import router as api_router

# Buat instance FastAPI
app = FastAPI(title="FastAPI Video AI Stream")

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti sesuai domain frontend kamu di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tambahkan router
app.include_router(ws_router)
app.include_router(api_router)

# Jalankan server FastAPI jika file ini dieksekusi langsung
if __name__ == "__main__":
    mp.set_start_method("spawn")  # Penting untuk multiprocessing di Windows/macOS
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
