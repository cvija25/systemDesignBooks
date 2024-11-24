from fastapi import FastAPI
import uvicorn

app = FastAPI()

def ratelimiter(func):
    async def wrapper():
        # TODO implement ratelimit algorithm
        return await func()
    return wrapper

@app.get("/hello")
@ratelimiter
async def hello():
    return {"message": "hello"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
