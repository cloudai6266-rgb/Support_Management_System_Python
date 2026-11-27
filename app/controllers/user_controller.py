
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


# Add a new user
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.save_user(
            db, user.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


# Get all users
@router.get("", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


# Get users by type
@router.get("/type/{user_type}", response_model=list[UserResponse])
def get_users_by_type(user_type: str, db: Session = Depends(get_db)):
    return user_service.get_users_by_type(db, user_type)


# Get a user by email
@router.get("/email", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Get a user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Update an existing user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    db: Session = Depends(get_db)
):
    try:
        user = user_service.update_user(
            db, user_id, updated_user.model_dump()
        )

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


# Delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_service.delete_user(db, user_id)
    return None
