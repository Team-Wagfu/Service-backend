# Routes

This document lists every route currently registered by `main.py`.

Base application metadata:

| Item | Value |
|------|-------|
| Framework | FastAPI |
| App title | Wagfu Service Backend |
| App version | 1.0.0 |
| Route source | `main.py`, `api/routes/v1/*.py` |

## Authentication

Most endpoints depend on `services.jwt.master.user_metadata` and require a valid bearer token. The authentication routes also set or clear an HTTP-only cookie named `Bearer`.

Unauthenticated routes:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check. Returns `{"status": "ok"}`. |
| `POST` | `/user/create` | Register user and set `Bearer` cookie. |
| `POST` | `/user/login` | Authenticate user and set `Bearer` cookie. |

Authenticated routes should be called with:

```http
Authorization: Bearer <token>
```

## Route Summary

| Method | Path | Auth | Request model | Response model / body | Status |
|--------|------|------|---------------|-----------------------|--------|
| `GET` | `/health` | No | None | `{"status": "ok"}` | `200` |
| `POST` | `/user/create` | No | `createUser` | `readUser`; sets `Bearer` cookie | `201` |
| `POST` | `/user/update` | Yes | `createUser` | `readUser`; refreshes `Bearer` cookie | `200` |
| `DELETE` | `/user/delete` | Yes | None | `"User deleted successfully"`; clears `Bearer` cookie | `200` |
| `POST` | `/user/login` | No | `loginUser` | `readUser`; sets `Bearer` cookie | `200` |
| `POST` | `/user/logout` | Yes | None | `"Logout successful"`; clears `Bearer` cookie | `200` |
| `POST` | `/profile/create` | Yes | `WriteDoctorProfile` \| `WriteFacilitatorProfile` \| `WritePetOwnerProfile` | `ReadDoctorProfile` \| `ReadFacilitatorProfile` \| `ReadPetOwnerProfile` | `200` |
| `POST` | `/profile/update` | Yes | `UpdatePetOwnerProfile` \| `UpdateDoctorProfile` \| `UpdateFacilitatorProfile` | `ReadDoctorProfile` \| `ReadFacilitatorProfile` \| `ReadPetOwnerProfile` | `200` |
| `POST` | `/pet/create` | Yes | `createPet` | `readPet` | `201` |
| `GET` | `/pet/list` | Yes | None | `list[readPet]` | `200` |
| `GET` | `/pet/{pet_id}` | Yes | Path: `pet_id` | `readPet` | `200` |
| `POST` | `/pet/update` | Yes | `updatePet` | `readPet` | `200` |
| `DELETE` | `/pet/delete/{pet_id}` | Yes | Path: `pet_id` | `{"message": "OK"}` | `200` |
| `POST` | `/pet/vaccination/create` | Yes | `createVaccination` | `readVaccination` | `201` |
| `GET` | `/pet/vaccination/list/{pet_id}` | Yes | Path: `pet_id` | `list[readVaccination]` | `200` |
| `POST` | `/pet/vaccination/update` | Yes | `updateVaccination` | `readVaccination` | `200` |
| `POST` | `/pet/medical/create` | Yes | `createMedicalRecord` | `readMedicalRecord` | `201` |
| `GET` | `/pet/medical/list/{pet_id}` | Yes | Path: `pet_id` | `list[readMedicalRecord]` | `200` |
| `GET` | `/pet/medical/doctor/list` | Yes | None | `list[readMedicalRecord]` | `200` |
| `POST` | `/pet/medical/update` | Yes | `updateMedicalRecord` | `readMedicalRecord` | `200` |
| `GET` | `/poll/status` | Yes | Query: `poll_type?: int` | `PollStatusResponse` | `200` |
| `POST` | `/poll/notification/send` | Yes | `SendNotification` | `Notification` | `201` |
| `GET` | `/poll/notification/list` | Yes | Query: `unread_only: bool = false` | `NotificationList` | `200` |
| `POST` | `/poll/notification/ack` | Yes | `NotificationAck` | `Notification` or `null` | `200` |
| `GET` | `/token/token` | Yes | None | `readUser` | `200` |

## Route Details

### Health

#### `GET /health`

Simple application health check.

**Response**

```json
{
  "status": "ok"
}
```

### Users

Routes are defined in `api/routes/v1/auth.py` with prefix `/user` and tag `user`.

#### `POST /user/create`

Creates a user through `AuthService.register`, creates a JWT, and stores it in the HTTP-only `Bearer` cookie.

**Request:** `createUser`

**Response:** `201 Created` - `readUser`

#### `POST /user/update`

Updates the authenticated user through `UserRepository.update_user`, commits the change, creates a new JWT, and refreshes the `Bearer` cookie.

**Authentication:** required

**Request:** `createUser`

**Response:** `200 OK` - `readUser`

#### `DELETE /user/delete`

Soft-deletes the authenticated user, deletes the linked profile when possible, commits the change, and removes the `Bearer` cookie.

**Authentication:** required

**Response:** `200 OK` - text body `User deleted successfully`

#### `POST /user/login`

Authenticates by email and password through `AuthService.login`, creates a JWT, and stores it in the HTTP-only `Bearer` cookie.

**Request:** `loginUser`

**Response:** `200 OK` - `readUser`

#### `POST /user/logout`

Clears the `Bearer` cookie for the authenticated user.

**Authentication:** required

**Response:** `200 OK` - text body `Logout successful`

### Profiles

Routes are defined in `api/routes/v1/profile.py` with prefix `/profile`.

#### `POST /profile/create`

Creates a profile shape based on the submitted profile schema.

**Authentication:** required

**Request:** one of:

| Model |
|-------|
| `WriteDoctorProfile` |
| `WriteFacilitatorProfile` |
| `WritePetOwnerProfile` |

**Response:** one of `ReadDoctorProfile`, `ReadFacilitatorProfile`, or `ReadPetOwnerProfile`.

#### `POST /profile/update`

Updates a profile shape based on the submitted update schema.

**Authentication:** required

**Request:** one of:

| Model |
|-------|
| `UpdatePetOwnerProfile` |
| `UpdateDoctorProfile` |
| `UpdateFacilitatorProfile` |

**Response:** one of `ReadDoctorProfile`, `ReadFacilitatorProfile`, or `ReadPetOwnerProfile`.

### Pets

Routes are defined in `api/routes/v1/pets.py` with prefix `/pet` and tag `pet`.

See [pet_module.md](./pet_module.md) for the full pet module behavior.

#### `POST /pet/create`

Creates a pet under the authenticated owner's profile.

**Authentication:** required

**Request:** `createPet`

**Response:** `201 Created` - `readPet`

#### `GET /pet/list`

Lists pets for the authenticated owner.

**Authentication:** required

**Response:** `200 OK` - `list[readPet]`

#### `GET /pet/{pet_id}`

Fetches one pet by ID.

**Authentication:** required

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `pet_id` | string | Pet ID, usually `PET-{YYYY}-{NNNNN}`. |

**Response:** `200 OK` - `readPet`

#### `POST /pet/update`

Updates a pet.

**Authentication:** required

**Request:** `updatePet`

**Response:** `200 OK` - `readPet`

#### `DELETE /pet/delete/{pet_id}`

Deletes a pet.

**Authentication:** required

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `pet_id` | string | Pet ID, usually `PET-{YYYY}-{NNNNN}`. |

**Response:** `200 OK` - `{"message": "OK"}`

### Pet Add-ons

Routes are defined in `api/routes/v1/pet_addons.py` with prefix `/pet` and tags `pet`, `vaccination`, and `medical-records`.

See [pet_addons.md](./pet_addons.md) for authorization details and example payloads.

#### `POST /pet/vaccination/create`

Creates a vaccination schedule entry.

**Authentication:** required

**Request:** `createVaccination`

**Response:** `201 Created` - `readVaccination`

#### `GET /pet/vaccination/list/{pet_id}`

Lists vaccination records for a pet.

**Authentication:** required

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `pet_id` | string | Pet ID. |

**Response:** `200 OK` - `list[readVaccination]`

#### `POST /pet/vaccination/update`

Updates a vaccination record.

**Authentication:** required

**Request:** `updateVaccination`

**Response:** `200 OK` - `readVaccination`

#### `POST /pet/medical/create`

Creates a medical record.

**Authentication:** required

**Request:** `createMedicalRecord`

**Response:** `201 Created` - `readMedicalRecord`

#### `GET /pet/medical/list/{pet_id}`

Lists medical records for a pet.

**Authentication:** required

**Path parameters**

| Name | Type | Description |
|------|------|-------------|
| `pet_id` | string | Pet ID. |

**Response:** `200 OK` - `list[readMedicalRecord]`

#### `GET /pet/medical/doctor/list`

Lists medical records authored by the authenticated doctor.

**Authentication:** required

**Response:** `200 OK` - `list[readMedicalRecord]`

#### `POST /pet/medical/update`

Updates a medical record.

**Authentication:** required

**Request:** `updateMedicalRecord`

**Response:** `200 OK` - `readMedicalRecord`

### Polling and Notifications

Routes are defined in `api/routes/v1/polling.py` with prefix `/poll` and tags `poll` and `notification-routing`.

See [notification.md](./notification.md) for short-polling behavior and example payloads.

#### `GET /poll/status`

Returns pending poll buckets for the authenticated user.

**Authentication:** required

**Query parameters**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `poll_type` | int | No | Optional `PollType` filter. |

**Response:** `200 OK` - `PollStatusResponse`

#### `POST /poll/notification/send`

Sends a notification from the authenticated user to another user.

**Authentication:** required

**Request:** `SendNotification`

**Response:** `201 Created` - `Notification`

#### `GET /poll/notification/list`

Lists notifications for the authenticated recipient.

**Authentication:** required

**Query parameters**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `unread_only` | bool | No | `false` | Return only unread notifications when `true`. |

**Response:** `200 OK` - `NotificationList`

#### `POST /poll/notification/ack`

Acknowledges or deletes a notification.

**Authentication:** required

**Request:** `NotificationAck`

**Response:** `200 OK` - `Notification` or `null`

### Token

Routes are defined in `api/routes/v1/token.py` with prefix `/token` and tag `token`.

#### `GET /token/token`

Reads the authenticated token metadata, fetches the linked user, and returns public user details.

**Authentication:** required

**Response:** `200 OK` - `readUser`

Note: the full path is `/token/token` because the router prefix is `/token` and the route path is also `/token`.

## Error Handling

Global exception handlers are registered from `exception_handler.py`. Route errors are mapped from domain exceptions such as authentication, pet access, notification, vaccination, and medical record errors.

FastAPI/Pydantic validation errors are handled globally as `RequestValidationError` or `ValidationError`.
