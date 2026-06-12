import httpx
import uuid
import sys

from config import config

BASE_URL=config.url

def run_test():
    client = httpx.Client(base_url=BASE_URL)
    
    unique_suffix = str(uuid.uuid4())[:8]
    email = f"test_{unique_suffix}@example.com"
    password = "SuperPassword123!"
    name = f"Test User {unique_suffix}"
    
    print(f"1. Creating user {email}...")
    register_payload = {
        "name": name,
        "email": email,
        "pwd": password,
        "pwd_cnf": password,
        "type": "owner",
        "location": {"lat": 12.9716, "lng": 77.5946},
        "address": {
            "address_line_1": "12A",
            "address_line_2": "Near park",
            "street": "Main Road",
            "locality": "Indiranagar",
            "city": "Bengaluru",
            "district": "Bengaluru",
            "state": "Karnataka",
            "postal_code": 560001,
            "country": "IN"
        }
    }
    
    # 1. Create User
    res = client.post("/user/create", json=register_payload)
    if res.status_code != 201:
        print(f"[-] Registration failed with status {res.status_code}: {res.text}")
        sys.exit(1)
    
    data = res.json()
    print(f"[+] Registration successful: {data}")
    profile_id = data["profile_id"]
    
    # Check cookie
    bearer_cookie = client.cookies.get("Bearer")
    if not bearer_cookie:
        print("[-] Bearer cookie not found in response!")
        sys.exit(1)
    print(f"[+] Cookie found: Bearer={bearer_cookie[:20]}...")
    
    # 2. Get Token (verify session and email matching)
    print("2. Fetching user info from /token/token using the Bearer cookie...")
    res = client.get("/token/token")
    if res.status_code != 200:
        print(f"[-] /token/token failed with status {res.status_code}: {res.text}")
        sys.exit(1)
    
    token_data = res.json()
    print(f"[+] Token query returned: {token_data}")
    assert token_data["email"] == email
    assert token_data["profile_id"] == profile_id
    
    # 3. Logout
    print("3. Logging out...")
    res = client.post("/user/logout")
    if res.status_code != 200:
        print(f"[-] Logout failed with status {res.status_code}: {res.text}")
        sys.exit(1)
    
    bearer_cookie_after_logout = client.cookies.get("Bearer")
    print(f"[+] Logout response. Bearer cookie after logout: {bearer_cookie_after_logout}")
    
    # 4. Login
    print("4. Logging in back...")
    login_payload = {
        "email": email,
        "pwd": password
    }
    # Clear client cookies to verify login returns a new cookie
    client.cookies.clear()
    res = client.post("/user/login", json=login_payload)
    if res.status_code != 200:
        print(f"[-] Login failed with status {res.status_code}: {res.text}")
        sys.exit(1)
        
    login_data = res.json()
    print(f"[+] Login response: {login_data}")
    assert login_data["email"] == email
    
    new_bearer_cookie = client.cookies.get("Bearer")
    if not new_bearer_cookie:
        print("[-] Login did not return a Bearer cookie!")
        sys.exit(1)
    print(f"[+] New Bearer cookie set: {new_bearer_cookie[:20]}...")
    
    # 5. Delete User
    print("5. Deleting user...")
    res = client.delete("/user/delete")
    if res.status_code != 200:
        print(f"[-] Deletion failed with status {res.status_code}: {res.text}")
        sys.exit(1)
        
    print("[+] Deletion response: ", res.text)
    
    print("\n[***] ALL TESTS PASSED SUCCESSFULLY! [***]")

if __name__ == "__main__":
    run_test()
