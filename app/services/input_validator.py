from app.schemas.user_input import UserRequest, IngredientQuantity, Ingredients
import re

def validate_user_request(user_request: UserRequest) -> UserRequest:
    if user_request.preferences.ingredients:
        for ingredient in user_request.preferences.ingredients:
            ingredient.quantity = parse_quantity(ingredient.quantity.raw)
    
    # Add additional validation logic here, for example:
    valid_meal_types = ["breakfast", "lunch", "dinner", "snack"]
    if user_request.preferences.meal_type and user_request.preferences.meal_type not in valid_meal_types:
        raise ValueError(f"Invalid meal type. Must be one of {valid_meal_types}")
    
    # ... additional validation for other fields ...

    return user_request

def parse_quantity(raw_quantity: str) -> IngredientQuantity:
    """
    The function to parse the quantity of the ingredient
    This includes a simple regex to extract the amount and unit from the raw string by matching the amount and unit patterns.
    """
    match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)', raw_quantity.strip())
    if match:
        amount = float(match.group(1))                                     # Strips the amount to a float
        unit = match.group(2).strip() if match.group(2) else None          # Strips the unit to a string
    return IngredientQuantity(raw=raw_quantity, amount=amount, unit=unit)



