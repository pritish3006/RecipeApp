# Importing the necessary libraries
from pydantic import BaseModel, Field
from typing import List, Optional


class Ingredients(BaseModel):
    """
    The ingredients of the recipe
    """
    # The name of the ingredient
    name: str = Field(..., description="The name of the ingredient", examples=["tomato", "onion", "garlic"])
    # The quantity of the ingredient
    quantity: Optional[float] = Field(None, description="The quantity of the ingredient", examples=["1", "2", "3"])
    # The unit of the quantity
    unit: Optional[str] = Field(None, description="The unit of the quantity", examples=["cup", "tablespoon", "clove"])

class UserPreferences(BaseModel):
    """
    The preferences of the user
    """
    # The dietary restrictions of the user
    dietary_restrictions: Optional[List[str]] = Field(None, description="The dietary restrictions of the user", examples=["vegan", "gluten-free", "keto"])
    cuisine: Optional[str] = Field(None, description="The cuisine of the recipe", examples=["Italian", "Mexican", "French"])
    meal_type: Optional[str] = Field(None, description="The type of meal", examples=["breakfast", "lunch", "dinner"])
    intolerances: Optional[List[str]] = Field(None, description="The intolerances of the user", examples=["dairy", "gluten", "peanuts"])
    allergies: Optional[List[str]] = Field(None, description="The allergies of the user", examples=["eggs", "seafood", "soy"])
    preferences: Optional[List[str]] = Field(None, description="The preferences of the user", examples=["spicy", "sweet", "sour"])
    ingredients: Optional[List[Ingredients]] = Field(None, description="The ingredients of the recipe")

class UserRequest(BaseModel):
    """
    The request of the user
"""
    ingredients: List[Ingredients]
    preferences: Optional[UserPreferences] = None