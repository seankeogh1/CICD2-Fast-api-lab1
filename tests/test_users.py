import pytest

def user_payload( name="Paul", email="paul@atu.ie", age=26, student_id="S1234567"):
    return {"name": name, "email": email, "age": age, "student_id": student_id}

def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1


def test_duplicate_user_id_returns_409(client):
    client.post("/api/users", json=user_payload())

    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 409
    assert "exists" in response.json()["detail"].lower()

@pytest.mark.parametrize("bad_student_id", ["1234567", "s1234567", "S123", "S12345678"])

def test_bad_student_id_returns_422(client, bad_student_id):
    response = client.post("/api/users", json=user_payload(student_id=bad_student_id))
    assert response.status_code == 422

def test_get_users_returns_created_users(client): 
    client.post("/api/users", json=user_payload(name="Alice", email="alice@atu.ie")) 
 
    response = client.get("/api/users") 
    user_id = response.json()[0]["id"]
    assert response.status_code == 200 
    data = response.json() 
    assert len(data) == 1 
    assert data[0]["id"] == user_id
    assert data[0]["name"] == "Alice" 

def test_get_existing_user_returns_200(client): 
    data= client.post("/api/users", json=user_payload()) 
    user_id = data.json()["id"]
    response = client.get(f"/api/users/{user_id}") 
 
    assert response.status_code == 200 
    assert response.json()["id"] == user_id 

def test_get_missing_user_returns_404(client): 
    response = client.get("/api/users/999") 
 
    assert response.status_code == 404 
    assert response.json()["detail"] == "User not found" 

def test_delete_user(client): 
    created = client.post( 
        "/api/users", 
        json=user_payload(), 
    ).json() 
 
    user_id = created["id"] 
 
    response = client.delete(f"/api/users/{user_id}") 
    assert response.status_code == 204 
 
    response = client.get(f"/api/users/{user_id}") 
    assert response.status_code == 404 
 
 




