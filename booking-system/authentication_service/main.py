from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from auth.routers import user_router


# An instance of FastAPI (for authentication service)
authentication_app = FastAPI()

# Attaching routers to authentication_app
authentication_app.include_router(user_router)

# CORS for frontend(soon)
origins = []
authentication_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
