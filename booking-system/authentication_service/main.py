from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from auth.routers import router as user_auth_router


# An instance of FastAPI (for authentication service)
authentication_app = FastAPI()


# Attaching routers to authentication_app
authentication_app.include_router(user_auth_router)

# Middleware for logging requests (optional, for debugging)
@authentication_app.middleware("http")
async def log_requests(request: Request, call_next):
    origin = request.headers.get("origin")
    referer = request.headers.get("referer")
    print(f"Request: {request.method} {request.url}, Origin: {origin}, Referer: {referer}")
    response = await call_next(request)
    return response


# CORS for frontend(soon)
origins = ["http://localhost:8002", "http://localhost:8003"]
authentication_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
