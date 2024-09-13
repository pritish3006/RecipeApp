from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi_redis_cache import FastApiRedisCache, cache
from app.api import user_input
import logging
import os
from contextlib import asynccontextmanager
from fastapi import APIRouter

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )
logger = logging.getLogger(__name__)

# Redis cache setup
redis_cache = FastApiRedisCache()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("Starting up Recipe Generator API")
    redis_cache.init(
        host_url = os.environ.get("REDIS_URL", "redis://localhost:6379"), 
        prefix = "best_recipe_api-Cache",
        response_header = "X-BestRecipeAPI-Cache",
        debug = True,
        ignore_arg_types = [Request, Response, Session],  # Added comma here
        ttl = 30 * 60,  # 30 minutes
    )
    yield
    # shutdown
    logger.info("Shutting down Recipe Generator API")
    redis_cache.close()

# Initialize FastAPI app
app = FastAPI(title = "Best Recipe API", description = "API for Best Recipe App Ever")

api_router = APIRouter(prefix="/api/v1")

app.include_router(user_input.router, prefix="/api/v1")                                 # Include the user_input router and set the prefix to /api/v1

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom exception handler for HTTP exceptions.

    This function handles HTTP exceptions and returns a JSON response with the exception details.

    Args:
        request (Request): The incoming request object.
        exc (HTTPException): The HTTP exception that occurred.

    Returns:
    
    """
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})



@app.get("/")
async def root():
    """
    Root endpoint for the Best Recipe API.

    Returns:
        dict: A welcome message for the API.

    Example:
        Response:
        {
            "message": "Welcome to the Best Recipe API"
        }
    """
    logger.info("Root endpoing accessed")
    return {"message": "Welcome to the Best Recipe API"}

@app.get("/api/v1/health")
async def health_check():
    """
    Check the health of the API.

    Returns:
        dict: A status message indicating the API is healthy.

    Example:
        Response:
        {
            "status": "ok",
            "message": "API is healthy"
        }
    """
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "message": "API is healthy"}

if __name__ == "__main__":
    # Run the API using Uvicorn
    import uvicorn
    # Configure Uvicorn to run the FastAPI application
    #
    # This section sets up the Uvicorn server to run our FastAPI application.
    # We use the following configuration:
    # - app: The FastAPI application instance
    # - host: "0.0.0.0" to make the server accessible from any IP address
    # - port: 8000, the standard port for development servers
    #
    # Running the application this way allows for easy debugging and testing
    # during development. For production deployment, consider using a proper
    # ASGI server setup with appropriate security measures.
    logger.info("Starting Best recipe App")
    uvicorn.run(app, host="0.0.0.0", port=8000)



