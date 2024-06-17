from fastapi import FastAPI


app = FastAPI()


@app.get('/')  # Decorator
async def root():  # Name these function as descriptive as possible
    return {"message": "Hello world"}
