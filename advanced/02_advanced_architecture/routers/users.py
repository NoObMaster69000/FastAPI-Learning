from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_query_token

router = APIRouter()

@router.get("/")
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/me")
def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/{username}")
def read_user(username: str):
    return {"username": username}
