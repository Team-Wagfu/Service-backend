# Wagfu service backend
# custom annotated types
# Updated 1 May 2026

from enum import Enum
from typing import Annotated, TypedDict, Callable
from pydantic import AfterValidator, Field, TypeAdapter


__all__=["PetID", "DocID", "PetOwnerID", "PharmaceuticalID", "ClinicID", "MedicalRecordID", "PhoneNumber", "Location", "IdTypeAdapter"]

# validator for id prefix
def prefix(prefix: str)-> Callable[[str], str]:

	''' generates a validator function object
	that validated if the given string satisfies the given conditions
	along with the given prefix

	Example:
		prefix('abc') -> function

		function: verifies if the passed string starts with the given prefix
		and follows the given format prefix-[4 digit]-[5 digit]
	'''

	def validator(value: str) -> str|None:
		if not value.startswith(prefix):
			raise ValueError(f'Id should start with {prefix}')

		sectors=value.split('-')[1:]
		if not (sectors[0].isdigit() and sectors[1].isdigit()):
			raise ValueError(f'Id parse failure, format error, prefix: {value}, l1')

		if len(sectors[-1])!=5 or len(sectors[0])!=4 or len(sectors)!=2:
			raise ValueError(f'Id parse failure, format error, prefix: {value}, l2')

		if not int(sectors[-1]):
			raise ValueError('Invalid ID, 00000')

		return value

	return validator

# validate phone number
def phone_number_validator(v: str) -> str: # TODO

	''' verify if the given phone number is valid or not
	checking thru patterns to see if any of it matches
	'''

	cleaned=re.sub(r'[\s\-$$$$]','',v)

	if not cleaned.isdigit():
		raise ValueError("Phone number must contain only digits")

	if len(cleaned)!=10:
		raise ValueError("Phone number must be 10 digits")

	if not re.match(r'^(\+91|0)?[6-9]\d{9}$', cleaned):
		raise ValueError("Invalid Phone number")

	return cleaned

# coordinate dictionary
class CoordinateDict(TypedDict):
    lat: Annotated[float, Field(..., ge=-90, le=90)]
    lng: Annotated[float, Field(..., ge=-180, le=180)]


# geolocation coordinates validator
def geolocation_validator(v: CoordinateDict) -> CoordinateDict:

    ''' verify whether the given coordinatess are valid or not '''
    return v


def phone_number_optional_validator(v: str) -> str: # TODO

	''' verify phone number if provided, else just ignore it '''
	return v

def geolocation_optional_validator(v: CoordinateDict) -> CoordinateDict: # TODO

	''' verify coordinated if provided the coordinates, else ignore it'''
	return v

# ID types
PetID=Annotated[str, AfterValidator(prefix('PET'))]
DocID=Annotated[str, AfterValidator(prefix('DOC'))]
PetOwnerID=Annotated[str, AfterValidator(prefix('PW'))]
PharmaceuticalID=Annotated[str, AfterValidator(prefix('PHM'))]
ClinicID=Annotated[str, AfterValidator(prefix('CLN'))]
MedicalRecordID=Annotated[str, AfterValidator(prefix('MED'))]
PetPassportID=Annotated[str, AfterValidator(prefix('PPA'))]

# OTHER TYPES
# type to accommondate phone numbers and validate them
PhoneNumber=Annotated[str, AfterValidator(phone_number_validator)]
PhoneNumberOptional=Annotated[str, AfterValidator(phone_number_optional_validator)]

# Location Type
# to identify patient locality and clinic locality
Location=Annotated[CoordinateDict, AfterValidator(geolocation_validator)]
LocationOptional=Annotated[CoordinateDict, AfterValidator(geolocation_optional_validator)]


# Collective Type Adapter Class
class IdTypeAdapter:
	pet=TypeAdapter(PetID)
	doc=TypeAdapter(DocID)
	petowner=TypeAdapter(PetOwnerID)
	pharma=TypeAdapter(PharmaceuticalID)
	clinic=TypeAdapter(ClinicID)
	medical=TypeAdapter(MedicalRecordID)
	petpassport=TypeAdapter(PetPassportID)

# address type enum (used in AddressDict)
class AddressType(str, Enum):
	home="home"
	billing="billing"
	em="emergency"


# address dict
class AddressDict(TypedDict):
	address_line_1: Annotated[str, Field(..., description="mandatory field, primary unit identifier")]
	address_line_2: Annotated[str, Field(default='', description="secondary information")]
	street: Annotated[str, Field(..., description="street/road name")]
	locality: Annotated[str, Field(..., description="Area/neighborhood/village")]
	city: Annotated[str, Field(..., description="City/Town")] # should check for validity
	district: Annotated[str, Field(..., description="Administrative district")] # should check for validity
	state: Annotated[str, Field(..., description="state/union teritory")]
	postal_code: Annotated[int, Field(..., gt=0, description="Postal code")]
	country: Annotated[str, Field(None, description="ISO standard country code")]
	coordinates: Annotated[Location, Field(None, description="Geocordinates in the specified format")]
	address_type: Annotated[AddressType, Field(default=AddressType.home, description="type of address, home/billing/emergency")]

# client info dict
class ClientInfo(TypedDict):
	name: Annotated[str, Field(..., min_length=3, max_length=50)]
	address: Annotated[AddressDict, Field(default_factory={})]
	contact: Annotated[PhoneNumber, Field(default='')]

# medical record format
# to be used when parsing medical record
class MedicalRecord(TypedDict):
	client_info: Annotated[ClientInfo, Field(...)]

