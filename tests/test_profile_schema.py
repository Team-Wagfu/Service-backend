"""
Tests for profile request schemas.
"""

import pytest
from pydantic import ValidationError

from core.enums import FacilityType
from core.types import FacilitatorLinks
from schemas.profile import (
    WriteDoctorProfile,
    WriteFacilitatorProfile,
    WritePetOwnerProfile,
)


pytestmark = pytest.mark.schema


def address_payload(**overrides):
    payload = {
        "address_line_1": "12A",
        "address_line_2": "Near park",
        "street": "Main Road",
        "locality": "Indiranagar",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "postal_code": 560001,
        "country": "IN",
    }
    payload.update(overrides)
    return payload


def base_profile_payload(**overrides):
    payload = {
        "location": {"lat": 12.9716, "lng": 77.5946},
        "address": address_payload(),
    }
    payload.update(overrides)
    return payload


def test_pet_owner_profile_accepts_minimal_payload_and_uses_isolated_pet_list():
    first_profile = WritePetOwnerProfile(**base_profile_payload())
    second_profile = WritePetOwnerProfile(**base_profile_payload())

    assert first_profile.user_id == ""
    assert first_profile.pet_ids == []
    assert first_profile.pet_ids is not second_profile.pet_ids
    assert first_profile.address.city == "bengaluru"


def test_pet_owner_profile_accepts_pet_owner_id():
    profile = WritePetOwnerProfile(
        **base_profile_payload(user_id="PW-1234-00001", pet_ids=["PET-1234-00001"])
    )

    assert profile.user_id == "PW-1234-00001"
    assert profile.pet_ids == ["PET-1234-00001"]


def test_profile_rejects_unknown_top_level_fields():
    with pytest.raises(ValidationError) as error:
        WritePetOwnerProfile(**base_profile_payload(unexpected=True))

    assert error.value.errors()[0]["type"] == "extra_forbidden"


def test_profile_instances_are_frozen():
    profile = WritePetOwnerProfile(**base_profile_payload())

    with pytest.raises(ValidationError) as error:
        profile.location = {"lat": 0, "lng": 0}

    assert error.value.errors()[0]["type"] == "frozen_instance"


@pytest.mark.parametrize(
    ("payload", "error_type"),
    [
        ({"user_id": "BAD-1234-00001"}, "value_error"),
        ({"address": address_payload(postal_code=0)}, "greater_than"),
        ({"address": address_payload(extra_field="ignored")}, None),
    ],
)
def test_common_profile_validation(payload, error_type):
    if error_type is None:
        profile = WritePetOwnerProfile(**base_profile_payload(**payload))

        assert not hasattr(profile.address, "extra_field")
        return

    with pytest.raises(ValidationError) as error:
        WritePetOwnerProfile(**base_profile_payload(**payload))

    assert any(item["type"] == error_type for item in error.value.errors())


def test_doctor_profile_validates_specialisation_and_experience():
    profile = WriteDoctorProfile(
        **base_profile_payload(
            user_id="DOC-1234-00001",
            specialisation="Dermatology",
            experience=12,
        )
    )

    assert profile.user_id == "DOC-1234-00001"
    assert profile.specialisation == "Dermatology"
    assert profile.experience == 12


@pytest.mark.parametrize(
    ("field", "value", "error_type"),
    [
        ("specialisation", "x" * 51, "string_too_long"),
        ("experience", -1, "greater_than_equal"),
        ("experience", 101, "less_than_equal"),
    ],
)
def test_doctor_profile_rejects_invalid_field_bounds(field, value, error_type):
    payload = base_profile_payload(specialisation="Veterinary Medicine")
    payload[field] = value

    with pytest.raises(ValidationError) as error:
        WriteDoctorProfile(**payload)

    assert any(item["type"] == error_type for item in error.value.errors())


def test_doctor_profile_defaults_experience_to_zero():
    profile = WriteDoctorProfile(
        **base_profile_payload(specialisation="Veterinary Medicine")
    )

    assert profile.experience == 0


def test_facilitator_profile_accepts_clinic_id_and_enum_value():
    profile = WriteFacilitatorProfile(
        **base_profile_payload(
            user_id="CLN-1234-00001",
            name="Wagfu Clinic",
            description="General pet care",
            type=FacilityType.CLINIC,
        )
    )

    assert profile.user_id == "CLN-1234-00001"
    assert profile.type == FacilityType.CLINIC.value
    assert isinstance(profile.links, FacilitatorLinks)


@pytest.mark.parametrize(
    ("field", "value", "error_type"),
    [
        ("name", "", "string_too_short"),
        ("name", "x" * 101, "string_too_long"),
        ("description", "x" * 151, "string_too_long"),
        ("type", "not-a-facility", "is_instance_of"),
    ],
)
def test_facilitator_profile_rejects_invalid_fields(field, value, error_type):
    payload = base_profile_payload(
        name="Wagfu Clinic",
        description="General pet care",
        type=FacilityType.CLINIC,
    )
    payload[field] = value

    with pytest.raises(ValidationError) as error:
        WriteFacilitatorProfile(**payload)

    assert any(item["type"] == error_type for item in error.value.errors())


def test_facilitator_profile_accepts_links_payload():
    profile = WriteFacilitatorProfile(
        **base_profile_payload(
            name="Wagfu Clinic",
            description="General pet care",
            type=FacilityType.CLINIC,
            links={
                "website": "https://example.com",
                "instagram": "@wagfu.clinic",
                "facebook": "@wagfuclinic",
                "linkedin": "@wagfu_clinic",
            },
        )
    )

    assert profile.links.website == "example.com"
    assert profile.links.instagram == "wagfu.clinic"
