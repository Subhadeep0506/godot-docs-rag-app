from fastapi import FastAPI

app = FastAPI()

@app.post("/query")
def generate_response():
    pass