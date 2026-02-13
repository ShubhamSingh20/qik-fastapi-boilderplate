"""Notes CRUD endpoints."""

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_note_service
from app.models import CreateNoteRequest, NoteResponse, UpdateNoteRequest
from app.service.notes import NoteService
from app.view.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[NoteResponse])
async def list_notes(
    current_user: Dict[str, Any] = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    """List all notes for the current user."""
    notes = await note_service.list_notes(current_user["id"])
    return [NoteResponse(**n) for n in notes]


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    request: CreateNoteRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    """Create a new note."""
    note = await note_service.create_note(
        user_id=current_user["id"],
        title=request.title,
        content=request.content,
    )
    return NoteResponse(**note)


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    """Get a single note by ID."""
    note = await note_service.get_note(note_id, current_user["id"])
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteResponse(**note)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    request: UpdateNoteRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    """Update a note (partial update -- only provided fields are changed)."""
    note = await note_service.update_note(
        note_id=note_id,
        user_id=current_user["id"],
        title=request.title,
        content=request.content,
    )
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteResponse(**note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    """Delete a note."""
    deleted = await note_service.delete_note(note_id, current_user["id"])
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
