# Recipe Generator

This application generates custom recipes based on user-provided ingredients and preferences.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - On Unix or MacOS: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`

## Running the application

```bash
uvicorn app.main:app --reload