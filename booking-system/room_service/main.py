from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from room.routers import router


# An instance of FastAPI (for authentication service)
room_app = FastAPI()

# Attaching routers to authentication_app
room_app.include_router(router)

# CORS for frontend(soon)
origins = []
room_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
