"""Authentication endpoints."""

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.dependencies import get_auth_service
from app.models import LoginRequest, TokenResponse, UserResponse
from app.service.auth import AuthService

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

router = APIRouter(tags=["Auth"])


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> Dict[str, Any]:
    """Dependency: resolve current user from JWT Bearer token. Raises 401 on failure."""
    if not credentials or credentials.credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = auth_service.decode_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/auth", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authenticate with email + password, receive a JWT."""
    user = await auth_service.authenticate(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = auth_service.create_access_token(user["id"])
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        created_at=current_user["created_at"],
        updated_at=current_user["updated_at"],
    )
