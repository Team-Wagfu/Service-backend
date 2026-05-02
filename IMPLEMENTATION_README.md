# 📌 Backend API Specification

This application is built using **React + Capacitor** and is currently **frontend-only**.
All data (patients, doctor profile, notifications) is stored locally in `portalData.js`.

To enable full functionality, a backend service must be implemented with the following **REST API endpoints**.

---

## 🩺 1. Doctor Profile

### 🔹 Get Doctor Profile

```http
GET /api/doctor/profile
```

**Description:**
Returns the doctor’s profile details.

**Response Fields:**

* Name
* Qualification
* Specialization
* Clinic
* Experience
* Email
* Phone
* Shift
* Location

---

## 🔔 2. Notifications

### 🔹 Get Notifications

```http
GET /api/notifications
```

**Description:**
Returns a list of notifications for the doctor.

---

### 🔹 Acknowledge Notification (Optional)

```http
POST /api/notifications/acknowledge
```

**Description:**
Marks a notification as read or acknowledged.

---

## 🐾 3. Patients

### 🔹 Get All Patients

```http
GET /api/patients
```

**Description:**
Returns a list of all patients.

**Fields:**

* petName
* ownerName
* passportId # is it necessary? why? justify...
* species
* breed
* age
* gender
* weight
* primaryConcern
* vaccinationStatus
* allergies
* currentMedication
* emergencyContact

---

### 🔹 Get Patient by ID

```http
GET /api/patients/:id
```

**Description:**
Returns detailed information for a specific patient, including:

* Medical history
* Appointments

---

### 🔹 Add New Patient

```http
POST /api/patients
```

---

### 🔹 Update Patient

```http
PUT /api/patients/:id
```

---

### Delete Patient

```http
DELETE /api/patients/:id
```

---

## 4. Patient History

### Get Patient History

```http
GET /api/patients/:id/history
```

**Description:**
Returns all medical history notes for a patient.

---

### Add History Note

```http
POST /api/patients/:id/history
```

issue: no, history shouldn't be mutable, it should be automatically  assigned and head movement handled internally

---

## 📅 5. Appointments

### 🔹 Get Appointments

```http
GET /api/patients/:id/appointments
```

**Description:**
Returns all appointments for a specific patient.

---

### 🔹 Create Appointment

```http
POST /api/patients/:id/appointments
```

---

### 🔹 Update Appointment

```http
PUT /api/appointments/:appointmentId
```

---

### 🔹 Delete Appointment

```http
DELETE /api/appointments/:appointmentId
```

---

# 🚀 Notes for Backend Implementation

* Use standard REST conventions
* JSON format for request/response
* Include proper status codes (`200`, `201`, `400`, `404`, etc.)
* Authentication (JWT/session) can be added if required
* Ensure data validation and error handling
