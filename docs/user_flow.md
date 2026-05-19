# USER
irrespective of the type of user, the entry point of any kind of user is the User,
from there it branches to 
- pet owner
    - pet profile is completed and the relation is made and committed
    - then relation(s) are made to the pets table(which is an independent table of pet data), to those pets that are owned by the owner
    - from pets the vaccination are marked, in the vaccination table(pets->vaccination)
    - from pets the medical records are linked as pets->medical records
- doctor
    - the doctor profile is completed and connection is set up among the relations
    - the pets that are treated by the doctor are marked as doctor->pets
    - vaccination handled by the doctor are marked as vaccinations->doctor
    - medical records by  a doctor are mentioned as medical_record->doctor
    - clinics owned by the doctor are marked as doctor->clinic, and vice versa
        - clinic information is filled and linked with the doctor
        - clinic employees who submitted request to join the group are accepted/rejected
    - if works in a clinic, the profile is submitted to the owner and waited for verfiication

- facilitator
    - facilitator profiie is verified and connected
    - non-doc entity that owns a clinic/medical facility
    - leads to the clinic as clinic->user and vise versa
    