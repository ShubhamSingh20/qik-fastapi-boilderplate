"""Pydantic request and response schemas."""

from typing import Optional

from pydantic import BaseModel


# Auth

class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: str
    updated_at: str


# Notes

class CreateNoteRequest(BaseModel):
    title: str
    content: Optional[str] = ""


class UpdateNoteRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str
    updated_at: str
