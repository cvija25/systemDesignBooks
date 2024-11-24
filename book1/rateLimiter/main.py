from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from time import time

app = FastAPI()

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests, window_seconds):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_log = {}

    async def dispatch(self, request: Request, call_next):
        current_time = time()
        client_ip = request.client.host

        if client_ip not in self.request_log:
            self.request_log[client_ip] = []

        self.request_log[client_ip] = [req_time for req_time in self.request_log[client_ip] if current_time - req_time < self.window_seconds]

        if len(self.request_log[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="too many requests")
        
        self.request_log[client_ip].append(current_time)
        print(self.request_log)
        return await call_next(request)

app.add_middleware(RateLimiterMiddleware, max_requests=5, window_seconds=60)

@app.get("/hello")
async def hello():
    return {"message": "hello"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
