from enum import Enum
from pydantic import AfterValidator
from typing import Annotated, Literal, Dict, Callable, TypedDict
from .enums import VehicleType

import re

## VALIDATORS

def password_validator(pwd: str) -> str:

	'''
	password constraints includes,
			. length > 8
			. contains atleast 1 special character 	(0001)
			. contains atleast 1 uppercase letter	(0010)
			. contains atleast 1 digit				(0100)
			. contains atleast 1 lowercase letter	(1000)
	'''

	class masks(int, Enum):
		schar = 0b0001
		uchar = 0b0010
		dchar = 0b0100
		lchar = 0b1000

	if not pwd:
		raise ValueError('Password cannot be empty')

	if pwd.__len__()<8:
		raise ValueError('Password length cannot be <8')

	if pwd.endswith(' ') or pwd.startswith(' '):
		raise ValueError('Password cannot start/end with \' \'')

	mask = 0b0000
	for char in pwd:
		if mask | masks.uchar != masks.uchar and char.isupper():
			mask|=masks.uchar
		elif mask | masks.lchar != masks.lchar and char.islower():
			mask|=masks.lchar
		elif mask | masks.dchar != masks.dchar and char.isdigit():
			mask|=masks.dchar
		elif mask | masks.schar != masks.schar and char in '~!@#$%^&*()_-+=/<>,.\'";;\\`|':
			mask|=masks.schar
	else:
		return pwd

def username_validator(v: str) -> str:

	'''
	username constraints include,
		. min length of 5
		. max length of 25
		. can contain special characters _.
	'''

	if not v:
		raise ValueError("Username cannot be empty")

	if v.startswith(' ') or v.endswith(' '):
		raise ValueError("Username cannot start/end with \' \'(spaces)")

	username_length = v.__len__()
	if username_length <5 or username_length>25:
		raise ValueError("Username length should be between 5 and 25")

	for char in v:
		if not char.isalnum() and char not in '_.':
			raise ValueError(f'Illegal character in username, \'{char}\'')
	else:
		return v

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
			raise ValueError('Id parse failure, format error')
		
		if len(sectors[-1])!=6 or len(sectors[0])!=4 or len(sectors)!=2:
			raise ValueError('Id parse failure, format error')
		
		if not int(sectors[-1]):
			raise ValueError('Invalid ID, 00000')

		return value
	return validator

def Geolocation_validator(v: Dict[Literal["lat","lng"], float]) -> Dict[Literal["lat","lng"], float]:
	
	# basic validation
	if not (v['lat']>=-90 and v['lat']<=90):
		raise ValueError("Latitude must be between -90 and 90")
	elif not (v['lng']>=-180 and v['lng']<=180):
		raise ValueError("Longitude must be between -180 and 180")
	
	# further improvements in validation includes, inspeciting geography
	# to validate the place, logically

	return v

def vehicle_number_validator(v: str) -> str:
	return v

def Address_validator(v: str) -> str:
	# TODO
	return v

def phone_number_validator(v: str) -> str:
	# verify if the given phone number is valid or not
	# checking thru patterns to see if any of it matches
	
	cleaned=re.sub(r'[\s\-$$$$]','',v)

	if not cleaned.isdigit():
		raise ValueError("Phone number must contain only digits")

	if len(cleaned)!=10:
		raise ValueError("Phone number must be 10 digits")

	if not re.match(r'^(\+91|0)?[6-9]\d{9}$', cleaned):
		raise ValueError("Invalid Phone number")

	return cleaned

def driver_liscence_validator(v: str) -> str:
	
	# TODO (chat dated 05/04/2026)
	return v



## TYPES

# other types
UsernameStr = Annotated[
	str,
	AfterValidator(username_validator)
]

PasswordStr = Annotated[
	str,
	AfterValidator(password_validator)
]

class IDs:

	'''ID Types'''
	
	PetID=Annotated[
		str,
		AfterValidator(prefix('PET'))
	]

	PetOwnerID = Annotated[
		str,
		AfterValidator(prefix('PW'))
	]

	EmergencyUserID = Annotated[
		str,
		AfterValidator(prefix('EME'))
	]

	DoctorID = Annotated[
		str,
		AfterValidator(prefix('DOC'))
	]

	AdminID = Annotated[
		str,
		AfterValidator(prefix('ADM'))
	]

	PharmaceuticalID = Annotated[
		str,
		AfterValidator(prefix('PHM'))
	]

	ClinicID = Annotated[
		str,
		AfterValidator(prefix('CLN'))
	]

	FacilityID = Annotated[
		str,
		AfterValidator(prefix('FAC'))
	]

	MedicalRecordID = Annotated[
		str,
		AfterValidator(prefix('MED'))
	]


class Location:
	GeoLocation = Annotated[
		Dict[
			Literal["lat","lng"],
			float
		],
		AfterValidator(Geolocation_validator)
	]

	# incomplete type
	Address = Annotated[
		str,
		AfterValidator(Address_validator)
	]

class Vehicle: # TODO
	VehicleNumber = Annotated[
		str,
		AfterValidator(vehicle_number_validator),
	]

	VehicleType = Annotated[
		VehicleType,
		AfterValidator(vehicle_number_validator)
	]

	# TODO, need to enforce TypedDict here.

	# VehicleCapacityMetrics = Annotated[
	# 	Dict[
	# 		Literal["dim"],
	# 		Dict[
	# 			Literal["height","width","length"],
	# 			float
	# 		]
	# 	],
	# 	Literal["weight"],
	# 	float
	# ]

	DriverLiscence = Annotated[
		str,
		AfterValidator(driver_liscence_validator)
	]

class Phone:
	PhoneNumber = Annotated[
		str,
		AfterValidator(phone_number_validator)
	]

__all__ = ["UsernameStr", "PasswordStr", "IDs", "GeoLocation"]