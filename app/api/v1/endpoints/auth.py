from fastapi import APIRouter, Request, Depends
from sqlmodel import Session
from app.services.google_auth import oauth
from app.db.session import get_session
from app.crud.user import get_user_by_email, create_user
from app.models.user import User
from app.core.security import create_access_token

router = APIRouter()

@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, session: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    email = user_info["email"]

    user = get_user_by_email(session, email)

    if not user:
        user = create_user(session, User(email=email, is_google_user=True))

    jwt_token = create_access_token({"sub": user.email})

    return {"access_token": jwt_token, "token_type": "bearer"}
