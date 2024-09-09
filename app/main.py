from fastapi import FastAPI

app = FastAPI(title = "Best Recipe API", description = "API for Best Recipe App Ever")

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
    return {"message": "Welcome to the Best Recipe API"}

@app.get("api/v1/health")
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
    uvicorn.run(app, host="0.0.0.0", port=8000)



