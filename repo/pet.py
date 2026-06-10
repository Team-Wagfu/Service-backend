"""
CRUD operations for pet creation, retrieval, and owner linkage.

NO COMMITS IN CRUD
"""

from datetime import date
from random import randint

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.pets import Pets
from models.profile import PetOwnerProfile
from schemas.pets import createPet, updatePet


class PetRepository:
    @staticmethod
    def generate_pet_id() -> str:
        id_num = str(randint(1, 99999)).zfill(5)
        return f"PET-{date.today().year}-{id_num}"

    @staticmethod
    def create_pet(pet: createPet, owner_id: str, session: Session) -> Pets:
        db_pet = Pets(
            pet_id=PetRepository.generate_pet_id(),
            owner_id=owner_id,
            name=pet.name,
            type=pet.type,
            breed=pet.breed,
            color=pet.color,
            weight=pet.weight,
            height=pet.height,
        )

        session.add(db_pet)
        session.flush()
        session.refresh(db_pet)

        return db_pet

    @staticmethod
    def get_owner_profile(owner_id: str, session: Session) -> PetOwnerProfile | None:
        stmt = select(PetOwnerProfile).where(PetOwnerProfile.id == owner_id)
        return session.scalar(stmt)

    @staticmethod
    def link_pet_to_owner(
        profile: PetOwnerProfile, pet_id: str, session: Session
    ) -> PetOwnerProfile:
        current_ids = list(profile.pet_ids or [])
        if pet_id not in current_ids:
            current_ids.append(pet_id)
            profile.pet_ids = current_ids
            session.flush()
            session.refresh(profile)

        return profile

    @staticmethod
    def unlink_pet_from_owner(
        profile: PetOwnerProfile, pet_id: str, session: Session
    ) -> PetOwnerProfile:
        current_ids = list(profile.pet_ids or [])
        if pet_id in current_ids:
            current_ids.remove(pet_id)
            profile.pet_ids = current_ids
            session.flush()
            session.refresh(profile)

        return profile

    @staticmethod
    def get_pet_by_id(pet_id: str, session: Session) -> Pets | None:
        stmt = select(Pets).where(Pets.pet_id == pet_id)
        return session.scalar(stmt)

    @staticmethod
    def get_pets_by_owner(owner_id: str, session: Session) -> list[Pets]:
        stmt = select(Pets).where(Pets.owner_id == owner_id)
        return list(session.scalars(stmt).all())

    @staticmethod
    def update_pet(pet_id: str, data: updatePet, session: Session) -> Pets | None:
        db_pet = PetRepository.get_pet_by_id(pet_id, session)
        if not db_pet:
            return None

        if data.name is not None:
            db_pet.name = data.name
        if data.breed is not None:
            db_pet.breed = data.breed
        if data.color is not None:
            db_pet.color = data.color
        if data.weight is not None:
            db_pet.weight = data.weight
        if data.height is not None:
            db_pet.height = data.height

        session.flush()
        session.refresh(db_pet)

        return db_pet

    @staticmethod
    def delete_pet(pet_id: str, session: Session) -> bool:
        db_pet = PetRepository.get_pet_by_id(pet_id, session)
        if not db_pet:
            return False

        session.delete(db_pet)
        session.flush()
        return True


__all__ = ["PetRepository"]
