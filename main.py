# main.py

import os
import json
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # UPDATED: Use a more current and available model name. This is the only line that changed.
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    full_prompt_text = f"{MASTER_PROMPT}{request.prompt}"

    try:
        response = model.generate_content(full_prompt_text)
        # Gemini API can return markdown JSON, so we need to clean it up
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        parsed_response = json.loads(cleaned_text)
        return parsed_response
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON from the generative model.")
    except Exception as e:
        # Pass the specific error from the API back to the user for better debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
