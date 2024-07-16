from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from booking.routers import router as booking_router


# An instance of FastAPI (for authentication service)
booking_app = FastAPI()

# Attaching routers to authentication_app
booking_app.include_router(booking_router)

# CORS for frontend(soon)
origins = []
booking_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
