import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

async def search_recipes(ingredients: List[str]) -> List[str]:
    """
        Search for recipe URLs basd on the ingredients provided by the user
    """
    # Setting this up with a placeholder
    return ["https://www.allrecipes.com/recipe/{i}" for i in range(1, 6)]                            # The way this is supposed to work is that it will return a list of URLs that are supposed to be scraped for recipe details

async def scrape_recipe(url: str) -> Dict:
    """
    Scrape the recipe details from the URL. 
    We use asyncio to handle the requests concurrently. 
    We are using a flexible approach here to handle different content types - JSON and HTML.
    """
    async with aiohttp.ClientSession() as session:
        headers = {"Accept": "application/json, text/html" }
        async with session.get(url) as response:
            if response.status == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:                                              # This is the case for if the URL is a REST API endpoint
                    data = await response.json()
                    return parse_json_recipe(data, url)                                             # Parse JSON data
                elif 'text/html' in content_type:                                                   # This is the case for if the URL is a web page
                    html = await response.text()
                    return parse_html_recipe(html, url)                                             # Parse HTML with BeautifulSoup
                else:
                    logger.error(f"Unsupported Content-Type: {content_type}")
                    return None
                # ... rest of the parsing logic
            else:
                logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                return None
    
def parse_json_recipe(data: Dict, url: str) -> Dict:
    """
    Parse the JSON recipe data from the URL.
    """
    return {
        "name": data.get("title", "Unknown Recipe"),
        "ingredients": data.get("ingredients"),
        "instructions": data.get("instructions"),
        "url": url
    }

def parse_html_recipe(html: str, url: str) -> Dict:
    """
    Parse recipe data from HTML format using BeautifulSoup.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    name = soup.find('h1').text if soup.find('h1') else "Unknown Recipe"
    ingredients = [li.text for li in soup.find_all('li', class_='ingredient')]
    instructions = [p.text for p in soup.find_all('p', class_='instruction')]

    return {
        "name": name,
        "ingredients": ingredients,
        "instructions": instructions,
        "url": url
    }

async def get_recipes(ingredients: List[str]) -> List[Dict]:
    """
    Main function to get recipes based on ingredients.
    """
    recipe_urls = await search_recipes(ingredients)
    recipes = []
    for url in recipe_urls:
        recipe = await scrape_recipe(url)
        if recipe:
            recipes.append(recipe)
    return recipes