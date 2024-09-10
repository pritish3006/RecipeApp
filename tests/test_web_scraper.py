import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.web_scraper import search_recipes, scrape_recipe, get_recipes

@pytest.mark.asyncio
async def test_search_recipes():
    """
    Test the search_recipes function.
    
    This test verifies that the search_recipes function returns a non-empty list of URLs
    when given a list of ingredients. Each URL should be a string.
    
    Note: This test uses mock data. When transitioning to actual websites, 
    replace the mock implementation with real API calls or web scraping logic.
    """
    ingredients = ["tomato", "onion", "garlic"]
    urls = await search_recipes(ingredients)
    assert len(urls) > 0
    assert all(isinstance(url, str) for url in urls)

@pytest.mark.asyncio
async def test_scrape_recipe():
    mock_url = "https://www.mockrecipesite.com/recipe/1"
    mock_html = """
    <html>
        <body>
            <h1>Mock Recipe Title</h1>
            <ul>
                <li>Ingredient 1</li>
                <li>Ingredient 2</li>
            </ul>
            <ol>
                <li>Step 1</li>
                <li>Step 2</li>
            </ol>
        </body>
    </html>
    """

    mock_response = MagicMock()
    mock_response.text.return_value = mock_html

    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response
        recipe = await scrape_recipe(mock_url)

    assert isinstance(recipe, dict)
    assert "title" in recipe
    assert "ingredients" in recipe
    assert "instructions" in recipe
    # Add more specific assertions based on your scrape_recipe implementation

@pytest.mark.asyncio 
async def test_get_recipes():
    """
    Test the get_recipes function.
    
    This test verifies that the get_recipes function can:
    1. Successfully return a list of recipes when given a list of ingredients.
    2. Handle exceptions thrown during the recipe scraping process.
    
    The test uses mocking to simulate both successful and failed recipe scraping.
    
    Note: When transitioning to actual websites:
    1. Consider adding integration tests that don't use mocks.
    2. Update the mock_recipe structure to match real scraped recipes.
    3. Adjust error handling tests based on actual error scenarios.
    """
    mock_recipe = {
        "name": "Mock Recipe",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": ["step1", "step2"]
    }

    # Test successful recipe retrieval
    with patch('app.services.web_scraper.scrape_recipe', new_callable=AsyncMock) as mock_scrape:
        mock_scrape.return_value = mock_recipe
        
        ingredients = ["tomato", "onion", "garlic"]
        recipes = await get_recipes(ingredients)
        
        assert len(recipes) > 0
        assert recipes[0] == mock_recipe
        assert mock_scrape.called

    # Test error handling
    with patch('app.services.web_scraper.scrape_recipe', new_callable=AsyncMock) as mock_scrape:
        mock_scrape.side_effect = Exception("Mocked error")

        with pytest.raises(Exception, match="Mocked error"):
            await get_recipes(ingredients)

