# Wagfu - Service Backend
# Profile fetch and manipulation endpoints
# updated: 26 Apr 2026

from fastapi import APIRouter, HTTPException

# configure export variables
__all__ = ["router"]

router = APIRouter(prefix="/profile")
