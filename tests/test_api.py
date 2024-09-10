from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Best Recipe API"}

def test_health_check():
    response = client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_submit_user_input():
    response = client.post("api/v1/recipes", json=
        {
        "preferences": {
            "dietary_restrictions": ["vegan"],
            "cuisine": "Italian",
            "meal_type": "dinner",
            "ingredients": [{"name": "tomato", "quantity": {"raw": "2 pieces"}}]
        }
    })
    assert response.status_code == 200
    assert "recipes" in response.json()
    assert "validated_request" in response.json()

def test_generate_recipes():
    response = client.post("api/v1/recipes", json=
        {
        "preferences": {
            "ingredients": [{"name": "tomato", "quantity": {"raw": "2 pieces"}},
                            {"name": "cheese", "quantity": {"raw": "100 grams"}}
                        ]
        }
    })
    assert response.status_code == 200
    assert "recipes" in response.json()
    assert "message" in response.json()