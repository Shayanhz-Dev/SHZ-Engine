from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.users.api.dependencies import get_user_service
from app.modules.users.service.user_service import UserService
from app.modules.users.schemas.user import RegisterRequest, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
        "/register",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED
    )
def register(
    data : RegisterRequest,
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = user_service.register(
            username=data.username,
            email=data.email,
            password=data.password
            )
        return user
    
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))