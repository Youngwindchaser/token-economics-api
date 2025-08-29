# main.py

import os
import json
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- FastAPI App Setup ---

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()

# --- CORS Configuration ---
# Define the list of "origins" (domains) that are allowed to access your API.
# The "*" wildcard allows all origins, which is fine for development
# but you might want to restrict this in production.
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:5500", # Common for VS Code Live Server
    "*", # Allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Your Master Prompt ---
MASTER_PROMPT = """
Analyze the following user prompt and optimize it for a Large Language Model.
Your goal is to make it more concise, clear, and token-efficient without losing the original intent.
Provide a JSON response with two keys: 'optimized_prompt' and 'analysis'.
The 'analysis' should be a brief, one-sentence explanation of the changes you made.

User Prompt:
"""

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Token Economics API!"}

@app.post("/optimize")
async def optimize_prompt(request: PromptRequest):
    model = genai.GenerativeModel('gemini-pro')
    full_prompt_text = f"{MASTER_PROMPT}{request.prompt}"

    try:
        response = model.generate_content(full_prompt_text)
        parsed_response = json.loads(response.text)
        return parsed_response
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON from the generative model.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")