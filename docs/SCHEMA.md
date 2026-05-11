# Wagfu Database Design Specification

This document outlines the architecture, relational mapping, and data constraints for the Wagfu application backend. It serves as the single source of truth for the database schema and programmatic validation.

---

## 1. Core Architecture Overview
The Wagfu database follows a **Base Identity + Profile Extension** pattern. 
- **Base Table**: `Users` serves as the primary registry for all entities.
- **Extension Tables**: Specialized tables (`Pet_Owner`, `Doctors`, etc.) extend the base user with specific attributes using a 1:1 relationship via `user_id`.
- **Relational Tables**: `Pets` functions as a child entity linked to owners.

---

## 2. Primary Entities

### 2.1 Users (Internal Identity)
The primary entry point for all system actors. Identifies the "Who".
- `user_id` (**UUID**): Primary Key.
- `type` (**Enum**): `UserType` (See §4.1).
- `display_name` (**String**): Display name for the user.

### 2.2 Pets (Child Table)
Stores individual pet profiles.
- `pet_id` (**String**): Formatted Unique ID (See §5.1). (slug PET)
- `name` (**String**): Pet name.
- `dob` (**Date**): Date of Birth of the pet.
- `type` (**Enum**): Species classification (See §4.2).
- `breed` (**String**): Specific breed from mapped options (See §4.3).
- `color` (**String**): Primary visual color (See §4.4).
- `weight` (**Float**): Weight in KG (decimal precision).
- `height` (**Float**): Height in CM (decimal precision).

### 2.3 Vaccination (Child Table)
- `pet_id` (**String**): Formatted Unique ID (See 5.1). (Slug PET)
- `vaccines` (**String**): Name of the vaccine
- `due_date` (**Date**): Date before which the vaccine should be aquired
- `status` (**Boolean**): Whether vaccine was aquired before the said date
- `vaccinated_at` (**String**): Name of the facility where the vaccination was taken from (NULLABLE, incase of not-aquired)
- `vaccinated_by` (**String**): Formatted Unique ID, Identifiacion of the doctor (Slug DOC)
- `vaccinated_on` (**Date**): Date at which the vaccination was completed (NULLABLE)
- `report` (**String**): Corresponding medical report id

> [!NOTE]
> The number of overdue days can be calculated by subtracting
> - due_date, if the vaccination wasn't completed yet
> - vaccinated_on, if vaccination was completed

### 2.4 MedicalRecords (Child Table)
- `pet_id` (**String**): Formatted Unique ID (See 5.1). (Slug PET)
- `medical_record_id` (**String**): Medical Record ID (Slug MED)
- `medical_history` (**Array/Text**): references MedicalRecords, array of diagnosis_id.
- `date` (**Date**): Date of issue of the medical record
- `file` (**String**): Path to the medical record file

> [!NOTE]
> Medical records are stored in file, following a specific format  
> implements a record parser to parse and do the appropriate actions

---

## 3. Profile Extension Tables (Derived Entities)

### 3.1 Pet_Owner (PW)
Extends base `Users` for customers.
- `user_id` (**UUID**): Foreign Key (Users).
- `owner_id` (**String**): Formatted ID (PW-slug).
- `location` (**JSONB**): Geo-coordinates or address.
- `pet_ids` (**JSONB**): List of associated `pet_id` strings.

### 3.2 Emergency (EME)
Logistics and mobile response units.
- `user_id` (**UUID**): Foreign Key (Users).
- `eme_id` (**String**): Formatted ID (EME-slug).
- `contact` (**String**): Emergency phone number.
- `vehicle_type` (**Enum**): e.g., Ambulance, Transport.
- `vehicle_reg_no` (**String**): License plate.
- `vehicle_capacity` (**Integer**): Payload/Space.
- `user_liscence` (**String**): License number of the user.
- `level` (**Integer**): [1-5] Capacity/Priority scale.
- `status` (**Enum**): `Available`, `Busy`, `Offline`.

### 3.3 Doctors (DOC)
Specialized medical professionals.
- `user_id` (**UUID**): Foreign Key (Users).
- `doc_id` (**String**): Formatted ID (DOC-slug).
- `clinic_ids` (**Array/Text**): Reference to `Clinics`, can be multiple.
- `specialization` (**String**): Medical focus area.
- `experience` (**Integer**): Years in practice.
- `rating` (**Float**): [0.0-10.0] aggregated score.
- `reviews` (**JSONB**): Array of review objects `{rating, comment}`.

### 3.4 Admin (ADM)
Internal management and operations.
- `user_id` (**UUID**): Foreign Key (Users).
- `admin_id` (**String**): Formatted ID (ADM-slug).
- `role` (**String**): Permission level (Master, Support, Moderator).
- `permissions` (**JSONB**): Specific action scopes.

### 3.5 Pharmaceuticals (PH)
Location and contact details of Pharmaceutical shops.
- `user_id` (**UUID**): Foreign Key (Users).
- `shop_id` (**String**): Formatted ID (PHM-slug).
- `license_no` (**String**): License number of the shop.
- `name` (**String**): Name of the shop.
- `owner_name` (**String**): Name of the owner.
- `contact` (**String**): Contact number.
- `location` (**JSONB**): Geo-coordinates or address.
- `rating` (**Float**): [0.0-10.0] aggregated score.
- `reviews` (**JSONB**): Array of review objects `{rating, comment}`.
- `level` (**Integer**): [1-5] Capacity/Priority scale. (1=low, 5=high)
- `verified` (**Boolean**): Whether the shop is verified, False unless explicitly marked as verified.

> [!NOTE] The license number of the shop is very important, it is used to verify the shop and to ensure that the shop is legitimate.

### 3.6 Clinics (CLN)
Information about clinics and their features, location, availability, etc.
- `clinic_id` (**String**): Formatted ID (CLN-slug).
- `clinic_name` (**String**): Name of the clinic.
- `location` (**JSONB**): Geo-coordinates or address.
- `facilities` (**Array/String**): Array of facility_id, references `Facilities`.
- `rating` (**Float**): [0.0-10.0] aggregated score.
- `reviews` (**Array/JSONB**): Array of review objects `{rating, comment}`.

> [!NOTE] Doctor <-> Clinic is a many-to-many relationship. Mapping implied through clinic_id

### 3.7 Facilities (FAC)
List of general facilites that can be used to map to clinics rather than having to store names as is.
- `facility_id` (**String**): Formatted ID (FAC-slug).
- `facility_name` (**String**): Name of the facility.
- `facility_description` (**String**): Description of the facility.
- `facility_type` (**String**): Type of the facility, general categorization. *eg. surgery, x-ray, ultrasound, laboratory, grooming, boarding, training, other.*

### 3.8 MedicalRecords (MED)
Details of each and every medical records.
- `diagnosis_id` (**String**): Formatted ID (MED-slug).
- `doctor_id` (**String**): Reference to `Doctors`.
- `notes` (**String**): Notes of the diagnosis.
- `diagnosis` (**String**): Diagnosis of the pet.
- `date` (**Date**): Date of the diagnosis.

---

## 4. Reference Enums & Mappings

### 4.1 User Types (UserType)
- `pet owner`
- `emergency` (Logistics/Mobile Units)
- `docs` (Medical/Clinics)
- `admin` (System Staff)
- `pharmaceuticals` (Pharmaceutical Shops)

### 4.2 Pet Species
- `DOG`, `CAT`, `BRD` (Bird), `FIH` (Fish), `REP` (Reptile), `RBT` (Rabbit), `OTH` (Other).

### 4.3 Breed Mappings
| Type        | Breeds Possible                                                                                    |
| :---------- | :------------------------------------------------------------------------------------------------- |
| **Dog**     | Labrador, German Shepherd, Golden Retriever, French Bulldog, Beagle, Poodle, Rottweiler            |
| **Cat**     | Persian, Maine Coon, Siamese, Ragdoll, Bengal, Sphynx, British Shorthair                           |
| **Bird**    | Budgie, Cockatiel, African Grey, Lovebird, Canary, Macaw, Cockatoo                                 |
| **Fish**    | Betta, Goldfish, Guppy, Molly, Angelfish, Neon Tetra, Oscar                                        |
| **Reptile** | Bearded Dragon, Leopard Gecko, Ball Python, Corn Snake, Red-Eared Slider, Veiled Chameleon, Iguana |
| **Rabbit**  | Holland Lop, Mini Rex, Netherland Dwarf, Lionhead, Flemish Giant, English Angora, Dutch Rabbit     |
| **Other**   | Hamster, Guinea Pig, Ferret, Chinchilla, Hedgehog, Sugarglider, Rat                                |

### 4.4 Color Mappings
| Type        | Colors Possible                                          |
| :---------- | :------------------------------------------------------- |
| **Dog**     | Black, White, Brown, Golden, Brindle, Cream              |
| **Cat**     | Black, White, Calico, Tabby, Ginger, Grey, Tortoiseshell |
| **Bird**    | Blue, Green, Yellow, Red, White, Multi-colored, Grey     |
| **Fish**    | Red, Blue, Gold, Silver, Orange, Spotted, Neon           |
| **Reptile** | Green, Brown, Yellow, Grey, Orange, Patterned, Black     |
| **Rabbit**  | White, Black, Grey, Cinnamon, Spotted, Agouti, Brown     |
| **Other**   | Grey, Cream, Brown, Black, White, Tan, Multi             |

---

## 5. System Logic & Formatting

### 5.1 ID Generation Protocol
Used for client-facing identity. Unlike internal UUIDs, these are reconstructable.
**Format**: `[Type-Slug]-[Year]-[5-digit-Padded-Integer]`

- **Slugs**: `PW`, `EME`, `DOC`, `ADM`, `PHM`, `VET`, `CLN`, `FAC`.
- **Validation**: Any 5-digit value of `00000` is invalid.
- **Example**: DOC-2026-00012, PW-2026-00012, EME-2026-00012, ADM-2026-00012, PH-2026-00012, VET-2026-00012, CLN-2026-00012, FAC-2026-00012
