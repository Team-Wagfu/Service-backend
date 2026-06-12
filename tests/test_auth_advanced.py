import pytest
import httpx
import uuid
from config import config

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def client():
    with httpx.Client(base_url=BASE_URL) as c:
        yield c

def test_duplicate_registration(client):
    unique_suffix = str(uuid.uuid4())[:8]
    email = f"dup_{unique_suffix}@example.com"
    password = "SuperPassword123!"
    
    payload = {
        "name": "Test User",
        "email": email,
        "pwd": password,
        "pwd_cnf": password,
        "type": "owner"
    }
    
    # First registration
    resp = client.post("/user/create", json=payload)
    assert resp.status_code == 201
    
    # Duplicate registration
    resp = client.post("/user/create", json=payload)
    # Based on exception_handler.py, UserExistsError returns 401 with redirect to /login
    assert resp.status_code == 401
    assert resp.json()["message"] == "Failed to register"

def test_login_invalid_credentials(client):
    email = "nonexistent@example.com"
    password = "wrongpassword"
    
    payload = {
        "email": email,
        "pwd": password
    }
    
    resp = client.post("/user/login", json=payload)
    # AuthenticationError returns 500 based on exception_handler.py
    assert resp.status_code == 500
    assert resp.json()["redirect"] == "/login"

def test_unauthorized_access(client):
    # Clear cookies
    client.cookies.clear()
    
    resp = client.get("/token/token")
    # FastAPI/HTTPBearer with auto_error=True returns 401 Unauthorized if missing
    assert resp.status_code == 401

def test_login_success_and_logout(client):
    unique_suffix = str(uuid.uuid4())[:8]
    email = f"success_{unique_suffix}@example.com"
    password = "SuperPassword123!"
    
    reg_payload = {
        "name": "Success User",
        "email": email,
        "pwd": password,
        "pwd_cnf": password,
        "type": "owner"
    }
    client.post("/user/create", json=reg_payload)
    
    # Login
    client.cookies.clear()
    login_payload = {"email": email, "pwd": password}
    resp = client.post("/user/login", json=login_payload)
    assert resp.status_code == 200
    assert "Bearer" in client.cookies
    
    # Logout
    resp = client.post("/user/logout")
    assert resp.status_code == 200
    
    print(f"\nDEBUG: Cookies after logout: {dict(client.cookies)}")
    
    # Re-fetch info to verify cookie is gone/invalid
    resp = client.get("/token/token")
    print(f"DEBUG: Response status after logout: {resp.status_code}")
    print(f"DEBUG: Response body: {resp.text}")
    assert resp.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])
