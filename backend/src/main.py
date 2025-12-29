"""
AURORA Tax Classifier - Main Entry Point

This is the main entry point for the FastAPI application.
Run with: uvicorn src.main:app --reload
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from .frameworks.fastapi_app import app

__all__ = ["app"]
