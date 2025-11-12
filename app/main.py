# task-service/app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.adapters.http import auth_router, items_router, health_router
from app.settings import settings
import logging # Import logging

log = logging.getLogger(__name__)

app = FastAPI(title="Task Service (Refactored)")

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    """
    Catches all business logic ValueErrors and returns a 400.
    e.g., "User already exists"
    """
    log.warning(f"Business logic error: {exc}") # Log it
    return JSONResponse(
        status_code=400,
        content={"error_type": "BusinessLogicError", "message": str(exc)},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catches ALL other 500 errors and returns a friendly response.
    """
    # Log the full error to the console (for debugging)
    log.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        # This is the "user-friendly" message
        content={"error_type": "InternalServerError", "message": "An internal server error occurred."},
    )

app.include_router(health_router.router)
app.include_router(auth_router.router)
app.include_router(items_router.router)

@app.get("/")
def root():
    return {"message": "Task Service is running"}
