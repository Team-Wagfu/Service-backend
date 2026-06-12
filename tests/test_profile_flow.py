import pytest
import httpx
import uuid

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def client():
    with httpx.Client(base_url=BASE_URL) as c:
        yield c

def test_pet_owner_profile_flow(client):
    # 1. Register a pet owner
    unique_suffix = str(uuid.uuid4())[:8]
    email = f"owner_{unique_suffix}@example.com"
    password = "SuperPassword123!"
    
    reg_payload = {
        "name": "Owner User",
        "email": email,
        "pwd": password,
        "pwd_cnf": password,
        "type": "owner"
    }
    resp = client.post("/user/create", json=reg_payload)
    assert resp.status_code == 201
    assert "Bearer" in client.cookies
    
    # 2. Complete/Create profile
    profile_payload = {
        "location": {"lat": 12.34, "lng": 56.78},
        "address": {
            "address_line_1": "123 Main St",
            "street": "MG Road",
            "locality": "Shivajinagar",
            "city": "Bangalore",
            "district": "Bangalore Urban",
            "state": "Karnataka",
            "postal_code": 560001
        },
        "pet_ids": []
    }
    
    resp = client.post("/profile/create", json=profile_payload)
    if resp.status_code != 201:
        print(f"DEBUG: Create Profile Failed: {resp.text}")
    assert resp.status_code == 201
    data = resp.json()
    assert data["address"]["city"] == "Bangalore"
    
    # 3. Update profile
    update_payload = {
        "id": data["id"], # Required by UpdatePetOwnerProfile
        "address": {
            "address_line_1": "123 Main St Updated",
            "street": "Palace Road",
            "locality": "Mysore",
            "city": "Mysore",
            "district": "Mysore District",
            "state": "Karnataka",
            "postal_code": 570001
        }
    }
    resp = client.post("/profile/update", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["address"]["city"] == "Mysore"

def test_doctor_profile_flow(client):
    # 1. Register a doctor
    unique_suffix = str(uuid.uuid4())[:8]
    email = f"doc_{unique_suffix}@example.com"
    password = "SuperPassword123!"
    
    reg_payload = {
        "name": "Doctor User",
        "email": email,
        "pwd": password,
        "pwd_cnf": password,
        "type": "doctor"
    }
    resp = client.post("/user/create", json=reg_payload)
    assert resp.status_code == 201
    
    # 2. Complete profile
    profile_payload = {
        "location": {"lat": 0, "lng": 0},
        "address": {
            "address_line_1": "Hospital Ave",
            "street": "Avenue 1",
            "locality": "Med Center",
            "city": "City",
            "district": "Med District",
            "state": "State",
            "postal_code": 111111
        },
        "specialisation": "Surgeon",
        "experience": 10
    }
    resp = client.post("/profile/create", json=profile_payload)
    if resp.status_code != 201:
        print(f"DEBUG: Create Doctor Profile Failed: {resp.text}")
    assert resp.status_code == 201
    data = resp.json()
    assert data["specialisation"] == "Surgeon"
    
    # 3. Update profile
    update_payload = {
        "id": data["id"],
        "experience": 11
    }
    resp = client.post("/profile/update", json=update_payload)
    assert resp.status_code == 200
    assert resp.json()["experience"] == 11

if __name__ == "__main__":
    pytest.main([__file__])
