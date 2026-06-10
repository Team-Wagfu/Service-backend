"""
handle pet registration and owner linkage services
"""

from sqlalchemy.orm import Session

from core.enums import UserType
from core.exceptions import (
    PetError,
    PetNotFoundError,
    PetOwnerProfileError,
    PetAccessError,
)
from models.pets import Pets
from repo.pet import PetRepository as repo
from schemas.pets import createPet, readPet, updatePet


class PetService:
    @staticmethod
    def _to_read_pet(pet: Pets) -> readPet:
        return readPet(
            pet_id=pet.pet_id,
            owner_id=pet.owner_id,
            name=pet.name,
            type=pet.type,
            breed=pet.breed,
            color=pet.color,
            weight=pet.weight,
            height=pet.height,
        )

    @staticmethod
    def _resolve_owner_profile(owner_id: str, role: str, session: Session):
        if role != UserType.owner.value:
            raise PetAccessError()

        profile = repo.get_owner_profile(owner_id, session)
        if not profile:
            raise PetOwnerProfileError()

        return profile

    @staticmethod
    def create(
        pet: createPet, owner_id: str, role: str, session: Session
    ) -> readPet:
        try:
            profile = PetService._resolve_owner_profile(owner_id, role, session)
            db_pet = repo.create_pet(pet, profile.id, session)
            repo.link_pet_to_owner(profile, db_pet.pet_id, session)
            session.commit()

            return PetService._to_read_pet(db_pet)
        except (PetAccessError, PetOwnerProfileError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetError()
        finally:
            session.close()

    @staticmethod
    def list_by_owner(owner_id: str, role: str, session: Session) -> list[readPet]:
        try:
            PetService._resolve_owner_profile(owner_id, role, session)
            pets = repo.get_pets_by_owner(owner_id, session)

            return [PetService._to_read_pet(pet) for pet in pets]
        except (PetAccessError, PetOwnerProfileError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetError()
        finally:
            session.close()

    @staticmethod
    def get(pet_id: str, owner_id: str, role: str, session: Session) -> readPet:
        try:
            PetService._resolve_owner_profile(owner_id, role, session)
            db_pet = repo.get_pet_by_id(pet_id, session)

            if not db_pet or db_pet.owner_id != owner_id:
                raise PetNotFoundError()

            return PetService._to_read_pet(db_pet)
        except (PetAccessError, PetOwnerProfileError, PetNotFoundError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetError()
        finally:
            session.close()

    @staticmethod
    def update(
        data: updatePet, owner_id: str, role: str, session: Session
    ) -> readPet:
        try:
            PetService._resolve_owner_profile(owner_id, role, session)
            db_pet = repo.get_pet_by_id(data.pet_id, session)

            if not db_pet or db_pet.owner_id != owner_id:
                raise PetNotFoundError()

            updated = repo.update_pet(data.pet_id, data, session)
            if not updated:
                raise PetNotFoundError()

            session.commit()
            return PetService._to_read_pet(updated)
        except (PetAccessError, PetOwnerProfileError, PetNotFoundError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetError()
        finally:
            session.close()

    @staticmethod
    def delete(pet_id: str, owner_id: str, role: str, session: Session) -> None:
        try:
            profile = PetService._resolve_owner_profile(owner_id, role, session)
            db_pet = repo.get_pet_by_id(pet_id, session)

            if not db_pet or db_pet.owner_id != owner_id:
                raise PetNotFoundError()

            repo.unlink_pet_from_owner(profile, pet_id, session)
            repo.delete_pet(pet_id, session)
            session.commit()
        except (PetAccessError, PetOwnerProfileError, PetNotFoundError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetError()
        finally:
            session.close()
