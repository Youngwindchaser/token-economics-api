
from fastapi import FastAPI

app = FastAPI()

# This tells FastAPI that the function below is in charge of handling
# requests that go to the URL "/" using a GET method.
@app.get("/")
async def read_root():

    # FastAPI will automatically convert this Python dictionary into JSON.
    return {"message": "Welcome to the Token Economics API!"}