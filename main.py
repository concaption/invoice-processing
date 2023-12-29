"""
path: app/main.py
"""
import logging
import sys

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.scheduler import start as start_scheduler
from app.routers import main


def configure_logging():
    """
    Configure logging for the application
    """
    # Create a root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Create a formatter for formatting log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create a handler for logging to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the root logger
    root_logger.addHandler(stream_handler)

    # log into a file
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


configure_logging()


@asynccontextmanager
async def startup_event(app: FastAPI):
    """
    Start the scheduler
    """
    start_scheduler()
    yield


app = FastAPI(lifespan=startup_event)

app.include_router(main.router)
origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Configure your secret key
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
