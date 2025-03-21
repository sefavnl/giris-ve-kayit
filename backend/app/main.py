from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(title="User Auth API")

# CORS configuration
origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:5173",  # Vite React frontend
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://giris-ve-kayit-1.onrender.com",  # Deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Auth API"}

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 