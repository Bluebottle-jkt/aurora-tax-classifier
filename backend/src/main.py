"""
AURORA Tax Classifier - Main Entry Point

This is the main entry point for the FastAPI application.
Run with: uvicorn src.main:app --reload
"""

from .frameworks.fastapi_app import app

__all__ = ["app"]
