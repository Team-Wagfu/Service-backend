# Wagfu service backend
# common declarative base
# Updated 8 May 2026

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): pass

__all__=["Base"] # export base
