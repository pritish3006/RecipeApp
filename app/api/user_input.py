from fastapi import APIRouter, HTTPException
from app.schemas.user_input import UserRequest
from app.services.input_validator import validate_user_request
from app.services.web_scraper import get_recipes
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/user-input")
async def submit_user_input(user_request: UserRequest):
    try:
        validated_request = validate_user_request(user_request)
        return {"message": "User input received successfully", "validated_request": validated_request}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-recipes")
async def generate_recipes(user_request: UserRequest):
    try:
        validated_request = validate_user_request(user_request)
        
        ingredients = [ingredient.name for ingredient in validated_request.preferences.ingredients] if validated_request.preferences.ingredients else []
        
        recipes = await get_recipes(ingredients)
        
        if not recipes:
            logger.warning("No recipes found for the given ingredients")
            raise HTTPException(status_code=404, detail="No recipes found for the given ingredients")
        
        return {
            "message": "Recipes generated successfully",
            "recipes": recipes
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"An error occurred while processing the request: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal error occurred")