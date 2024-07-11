import logging
from fastapi import APIRouter, HTTPException, status
from .schemas import UserSchema
from .custom_exceptions import UserCreateException

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s'
)

# Use a logger for this module
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/jwt", 
    tags=["UserAuth Operations"]
)


@router.post("/auth/signup", summary="Create new user")
def create_user_handler(user_in: UserSchema):
    # Get user by email
    user = UserService.get_user_by_email(user_in.email)

    # If the user exists raise HTTPException
    if user:
        logger.warning(f"Attempted to create a user with an email that already exists: {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    try:
        # Create user using repository for user
        user_id = UserService.register_user(user_in)
        logger.info(f"User created successfully: {user_in.username}")
        return {
            "status_code": 200,
            "user": {
                "user_id": user_id,
                **user_in.model_dump()
                }
            }
    except UserCreateException as ex:
        logger.error(f"Failed to create a new user: {ex}", exc_info=True)
        return f"{ex}: failure to create new user"