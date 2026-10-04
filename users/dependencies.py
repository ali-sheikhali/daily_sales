from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.users.models import UserModels


bearer_schema = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_schema),
        db: Session = Depends(get_db),
    ):

    payload = decode_access_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid or expired token")


    user = db.query(UserModels).filter_by(id = int(payload["sub"])).first()

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not found")

    return user
