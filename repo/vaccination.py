"""
CRUD operations for pet vaccination records.

NO COMMITS IN CRUD
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.pets import Vaccination
from schemas.pet_addons import createVaccination, updateVaccination


class VaccinationRepository:
    @staticmethod
    def create_vaccination(
        session: Session, payload: createVaccination
    ) -> Vaccination:
        record = Vaccination(
            pet_id=payload.pet_id,
            vaccine=payload.vaccine,
            due_date=payload.due_date,
            status=False,
        )
        session.add(record)
        session.flush()
        session.refresh(record)
        return record

    @staticmethod
    def get_vaccination(
        session: Session, pet_id: str, vaccine: str
    ) -> Vaccination | None:
        stmt = select(Vaccination).where(
            Vaccination.pet_id == pet_id,
            Vaccination.vaccine == vaccine,
        )
        return session.scalar(stmt)

    @staticmethod
    def list_for_pet(session: Session, pet_id: str) -> list[Vaccination]:
        stmt = select(Vaccination).where(Vaccination.pet_id == pet_id)
        return list(session.scalars(stmt).all())

    @staticmethod
    def update_vaccination(
        session: Session,
        pet_id: str,
        vaccine: str,
        data: updateVaccination,
        doctor_id: str | None = None,
    ) -> Vaccination | None:
        record = VaccinationRepository.get_vaccination(session, pet_id, vaccine)
        if not record:
            return None

        if data.due_date is not None:
            record.due_date = data.due_date
        if data.status is not None:
            record.status = data.status
        if data.vaccinated_at is not None:
            record.vaccinated_at = data.vaccinated_at
        if data.vaccinated_on is not None:
            record.vaccinated_on = data.vaccinated_on
        if data.report is not None:
            record.report = data.report

        if data.status is True and doctor_id:
            record.vaccinated_by = doctor_id

        session.flush()
        session.refresh(record)
        return record

    @staticmethod
    def delete_vaccination(session: Session, pet_id: str, vaccine: str) -> bool:
        record = VaccinationRepository.get_vaccination(session, pet_id, vaccine)
        if not record:
            return False

        session.delete(record)
        session.flush()
        return True


__all__ = ["VaccinationRepository"]
