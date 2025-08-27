# main.py

from fastapi import FastAPI
# Import BaseModel from Pydantic to define the request structure
from pydantic import BaseModel

# Create our Pydantic model
class PromptRequest(BaseModel):
    prompt: str

# Create the FastAPI app instance
app = FastAPI()

# This is our original "Hello World" endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Token Economics API!"}

# This is our new endpoint for optimizing prompts
@app.post("/optimize")
async def optimize_prompt(request: PromptRequest):
    # For now, we'll just return the prompt we received
    # to confirm that the endpoint is working correctly.
    # In the next step, we'll add the Gemini API logic here.
    return {"optimized_prompt": request.prompt}