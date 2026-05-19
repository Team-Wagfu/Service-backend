# wagfu service backend
# handle click commands for create, drop and manipulate db
# Update 12 May 2026

from config import config

from models.base import Base
from models.user import User
from models.profile import AdminProfile, DoctorProfile, PetOwnerProfile
from models.pets import Pets, MedicalRecords, Vaccination

if __name__ == "__main__":
    Base.metadata.create_all(config.engine)
