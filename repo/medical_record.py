"""
CRUD operations for pet medical records.

NO COMMITS IN CRUD
"""

from datetime import date
from random import randint

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.pets import MedicalRecords
from schemas.pet_addons import createMedicalRecord, updateMedicalRecord


class MedicalRecordRepository:
    @staticmethod
    def generate_medical_id() -> str:
        id_num = str(randint(1, 99999)).zfill(5)
        return f"MED-{date.today().year}-{id_num}"

    @staticmethod
    def create_record(
        session: Session,
        payload: createMedicalRecord,
        doctor_id: str,
    ) -> MedicalRecords:
        record = MedicalRecords(
            medical_id=MedicalRecordRepository.generate_medical_id(),
            pet_id=payload.pet_id,
            doctor_id=doctor_id,
            diagnosis=payload.diagnosis,
            date=payload.record_date,
        )
        session.add(record)
        session.flush()
        session.refresh(record)
        return record

    @staticmethod
    def get_by_id(session: Session, medical_id: str) -> MedicalRecords | None:
        stmt = select(MedicalRecords).where(MedicalRecords.medical_id == medical_id)
        return session.scalar(stmt)

    @staticmethod
    def list_for_pet(session: Session, pet_id: str) -> list[MedicalRecords]:
        stmt = select(MedicalRecords).where(MedicalRecords.pet_id == pet_id)
        return list(session.scalars(stmt).all())

    @staticmethod
    def list_for_doctor(session: Session, doctor_id: str) -> list[MedicalRecords]:
        stmt = select(MedicalRecords).where(MedicalRecords.doctor_id == doctor_id)
        return list(session.scalars(stmt).all())

    @staticmethod
    def update_record(
        session: Session,
        medical_id: str,
        data: updateMedicalRecord,
    ) -> MedicalRecords | None:
        record = MedicalRecordRepository.get_by_id(session, medical_id)
        if not record:
            return None

        if data.diagnosis is not None:
            record.diagnosis = data.diagnosis
        if data.record_date is not None:
            record.date = data.record_date

        session.flush()
        session.refresh(record)
        return record

    @staticmethod
    def delete_record(session: Session, medical_id: str) -> bool:
        record = MedicalRecordRepository.get_by_id(session, medical_id)
        if not record:
            return False

        session.delete(record)
        session.flush()
        return True


__all__ = ["MedicalRecordRepository"]
