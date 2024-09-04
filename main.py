from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/send-message")
async def send_message(request: Request):
    data = await request.json()
    message = data.get("message", "No message provided")
    return {"Message": message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
