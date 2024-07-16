import logging

from fastapi import APIRouter


# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/booking", 
    tags=["Booking Operations"],
)