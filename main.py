"""FastAPI boilerplate entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import get_db
from app.view.auth import router as auth_router
from app.view.notes import router as notes_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB + migrations. Shutdown: close connection."""
    db = get_db()
    await db.init()
    yield
    await db.close()


app = FastAPI(
    title="FastAPI Boilerplate",
    description="A clean FastAPI boilerplate with JWT auth, async SQLite, and notes CRUD",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(notes_router)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {"message": "FastAPI Boilerplate", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
