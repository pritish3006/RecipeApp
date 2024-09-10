import pytest
from app.schemas.user_input import UserRequest, UserPreferences, Ingredients, IngredientQuantity
from app.services.input_validator import validate_user_request

def test_valid_user_request():
    request = UserRequest(
        preferences=UserPreferences(
            dietary_restrictions=["vegetarian"],
            cuisine="Italian",
            meal_type="dinner",
            ingredients=[
                Ingredient(name="tomato", quantity=IngredientQuantity(raw="2 pieces"))
            ]
        )
    )
    validated = validate_user_request(request)
    assert validated == request

def test_invalid_ingredient_quantity():
    request = UserRequest(
        preferences=UserPreferences(
            ingredients=[
                Ingredient(name="flour", quantity=IngredientQuantity(raw="-1 cup"))
            ]
        )
    )
    with pytest.raises(ValueError):
        validate_user_request(request)

def test_invalid_meal_type():
    request = UserRequest(
        preferences=UserPreferences(
            meal_type="invalid_meal"
        )
    )
    with pytest.raises(ValueError):
        validate_user_request(request)