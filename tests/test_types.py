# Wagfu Service Backend
# unittest - validating and testing types and models
# Updated 6 May 2026

import pytest
from pydantic import TypeAdapter
from core.types import (
        PetID,
        DocID,
        PetOwnerID,
        PharmaceuticalID,
        ClinicID,
        MedicalRecordID,    
    )

# define adapters
_petid=TypeAdapter(PetID)
_docid=TypeAdapter(DocID)
_petownerid=TypeAdapter(PetOwnerID)
_pharmaceuticalsid=TypeAdapter(PharmaceuticalID)
_medicalrecordid=TypeAdapter(MedicalRecordID)
_clinicid=TypeAdapter(ClinicID)

# test functions
@pytest.mark.types
def test_valid_types():
    assert _petid.validate_python('PET-2024-14834') == "PET-2024-14834"
    assert _docid.validate_python('DOC-2024-12837') == "DOC-2024-12837"
    assert _petownerid.validate_python('PW-2023-31820') == "PW-2023-31820"
    assert _pharmaceuticalsid.validate_python('PHM-8123-72311') == "PHM-8123-72311"
    assert _medicalrecordid.validate_python('MED-1293-71773') == "MED-1293-71773"
    assert _clinicid.validate_python('CLN-1238-87394') == "CLN-1238-87394"

@pytest.mark.types
def test_invalid_types():
    # petid
    with pytest.raises(ValueError):
        _petid.validate_python('PET-21231-1232')
        
    # docid
    with pytest.raises(ValueError):
        _docid.validate_python('DOC-38942-1234')
