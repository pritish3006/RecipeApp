# Importing the necessary libraries
from fastapi import APIRouter, HTTPException
from app.schemas.user_input import UserRequest
from app.services.input_validator import validate_user_input

# Creating the router
# The router is used to handle the requests from the user
router = APIRouter()

@router.post("/user_input")
async def user_input(user_request: UserRequest):
    """
    The endpoint for the user input
    """
    try: 
        # Validating the user request
        validated_request = validate_user_request(user_request)
        # Returning the response
        # This is where we will pass the validated request to the next service.
        return {"message": "User input received successfully", "validated_request": validated_request}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))