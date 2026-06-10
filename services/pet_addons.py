"""
Vaccination and medical record services wired to pets and doctors.
"""

from sqlalchemy.orm import Session

from core.enums import UserType
from core.exceptions import (
    PetAddonError,
    PetAddonAccessError,
    PetNotFoundError,
    VaccinationNotFoundError,
    MedicalRecordNotFoundError,
    PetOwnerProfileError,
)
from models.pets import MedicalRecords, Vaccination
from repo.medical_record import MedicalRecordRepository as medical_repo
from repo.pet import PetRepository as pet_repo
from repo.vaccination import VaccinationRepository as vaccination_repo
from schemas.pet_addons import (
    createMedicalRecord,
    createVaccination,
    readMedicalRecord,
    readVaccination,
    updateMedicalRecord,
    updateVaccination,
)
from models.profile import DoctorProfile


class PetAddonService:
    @staticmethod
    def _get_doctor_profile(profile_id: str, session: Session) -> DoctorProfile:
        from sqlalchemy import select

        stmt = select(DoctorProfile).where(DoctorProfile.id == profile_id)
        doctor = session.scalar(stmt)
        if not doctor:
            raise PetAddonAccessError("Doctor profile not found")
        return doctor

    @staticmethod
    def _assert_pet_readable(pet_id: str, profile_id: str, role: str, session: Session):
        pet = pet_repo.get_pet_by_id(pet_id, session)
        if not pet:
            raise PetNotFoundError()

        if role == UserType.owner.value and pet.owner_id != profile_id:
            raise PetAddonAccessError("Pet does not belong to this owner")
        elif role not in (UserType.owner.value, UserType.doctor.value):
            raise PetAddonAccessError()

        return pet

    @staticmethod
    def _assert_owner_pet(pet_id: str, profile_id: str, role: str, session: Session):
        if role != UserType.owner.value:
            raise PetAddonAccessError("Only pet owners can perform this action")

        pet = pet_repo.get_pet_by_id(pet_id, session)
        if not pet or pet.owner_id != profile_id:
            raise PetNotFoundError()

        return pet

    @staticmethod
    def _to_read_vaccination(record: Vaccination) -> readVaccination:
        return readVaccination(
            pet_id=record.pet_id,
            vaccine=record.vaccine,
            due_date=record.due_date,
            status=record.status,
            vaccinated_at=record.vaccinated_at or None,
            vaccinated_by=record.vaccinated_by or None,
            vaccinated_on=record.vaccinated_on,
            report=record.report or None,
        )

    @staticmethod
    def _to_read_medical(record: MedicalRecords) -> readMedicalRecord:
        return readMedicalRecord(
            medical_id=record.medical_id,
            pet_id=record.pet_id,
            doctor_id=record.doctor_id,
            diagnosis=record.diagnosis,
            date=record.date,
        )

    @staticmethod
    def create_vaccination(
        payload: createVaccination,
        profile_id: str,
        role: str,
        session: Session,
    ) -> readVaccination:
        try:
            if role == UserType.owner.value:
                PetAddonService._assert_owner_pet(
                    payload.pet_id, profile_id, role, session
                )
            elif role == UserType.doctor.value:
                PetAddonService._assert_pet_readable(
                    payload.pet_id, profile_id, role, session
                )
            else:
                raise PetAddonAccessError()

            existing = vaccination_repo.get_vaccination(
                session, payload.pet_id, payload.vaccine
            )
            if existing:
                raise PetAddonError("Vaccination schedule already exists for this vaccine")

            record = vaccination_repo.create_vaccination(session, payload)
            session.commit()
            return PetAddonService._to_read_vaccination(record)
        except (
            PetNotFoundError,
            PetAddonAccessError,
            PetAddonError,
            PetOwnerProfileError,
        ):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()

    @staticmethod
    def list_vaccinations(
        pet_id: str,
        profile_id: str,
        role: str,
        session: Session,
    ) -> list[readVaccination]:
        try:
            PetAddonService._assert_pet_readable(pet_id, profile_id, role, session)
            records = vaccination_repo.list_for_pet(session, pet_id)
            return [PetAddonService._to_read_vaccination(r) for r in records]
        except (PetNotFoundError, PetAddonAccessError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()

    @staticmethod
    def update_vaccination(
        payload: updateVaccination,
        profile_id: str,
        role: str,
        session: Session,
    ) -> readVaccination:
        try:
            PetAddonService._assert_pet_readable(
                payload.pet_id, profile_id, role, session
            )
            record = vaccination_repo.get_vaccination(
                session, payload.pet_id, payload.vaccine
            )
            if not record:
                raise VaccinationNotFoundError()

            doctor_id = None
            if role == UserType.owner.value:
                if payload.status is True or payload.vaccinated_on is not None:
                    raise PetAddonAccessError(
                        "Owners cannot mark vaccinations as administered"
                    )
                allowed = updateVaccination(
                    pet_id=payload.pet_id,
                    vaccine=payload.vaccine,
                    due_date=payload.due_date,
                )
                payload = allowed
            elif role == UserType.doctor.value:
                doctor = PetAddonService._get_doctor_profile(profile_id, session)
                doctor_id = doctor.id
            else:
                raise PetAddonAccessError()

            updated = vaccination_repo.update_vaccination(
                session,
                payload.pet_id,
                payload.vaccine,
                payload,
                doctor_id=doctor_id,
            )
            session.commit()
            return PetAddonService._to_read_vaccination(updated)
        except (
            PetNotFoundError,
            PetAddonAccessError,
            VaccinationNotFoundError,
        ):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()

    @staticmethod
    def create_medical_record(
        payload: createMedicalRecord,
        profile_id: str,
        role: str,
        session: Session,
    ) -> readMedicalRecord:
        try:
            if role != UserType.doctor.value:
                raise PetAddonAccessError("Only doctors can create medical records")

            doctor = PetAddonService._get_doctor_profile(profile_id, session)
            PetAddonService._assert_pet_readable(
                payload.pet_id, profile_id, role, session
            )

            record = medical_repo.create_record(session, payload, doctor.id)
            session.commit()
            return PetAddonService._to_read_medical(record)
        except (PetNotFoundError, PetAddonAccessError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()

    @staticmethod
    def list_medical_records_for_pet(
        pet_id: str,
        profile_id: str,
        role: str,
        session: Session,
    ) -> list[readMedicalRecord]:
        try:
            PetAddonService._assert_pet_readable(pet_id, profile_id, role, session)
            records = medical_repo.list_for_pet(session, pet_id)
            return [PetAddonService._to_read_medical(r) for r in records]
        except (PetNotFoundError, PetAddonAccessError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()

    @staticmethod
    def list_medical_records_for_doctor(
        profile_id: str,
        role: str,
        session: Session,
    ) -> list[readMedicalRecord]:
        try:
            if role != UserType.doctor.value:
                raise PetAddonAccessError()

            doctor = PetAddonService._get_doctor_profile(profile_id, session)
            records = medical_repo.list_for_doctor(session, doctor.id)
            return [PetAddonService._to_read_medical(r) for r in records]
        except PetAddonAccessError:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()

    @staticmethod
    def update_medical_record(
        payload: updateMedicalRecord,
        profile_id: str,
        role: str,
        session: Session,
    ) -> readMedicalRecord:
        try:
            if role != UserType.doctor.value:
                raise PetAddonAccessError("Only doctors can update medical records")

            doctor = PetAddonService._get_doctor_profile(profile_id, session)
            record = medical_repo.get_by_id(session, payload.medical_id)
            if not record:
                raise MedicalRecordNotFoundError()

            if record.doctor_id != doctor.id:
                raise PetAddonAccessError("Cannot update another doctor's record")

            updated = medical_repo.update_record(session, payload.medical_id, payload)
            session.commit()
            return PetAddonService._to_read_medical(updated)
        except (PetAddonAccessError, MedicalRecordNotFoundError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise PetAddonError()
        finally:
            session.close()
