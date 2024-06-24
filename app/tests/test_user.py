from app.models.user_model import User

def test_create_user(test_client):
    user_data = {
        "email": "test_create@email.com",
        "password": "testpassword",
        "name": "Test User"
    }

    response = test_client.post("/user", json=user_data)
    
    assert response.status_code == 200

    created_user = response.json()
    
    assert created_user["email"] == user_data["email"]
    assert created_user["name"] == user_data["name"]
    

def test_create_user_email_duplicate(test_client):

    user_data = {
        "email": "test_conflict@email.com",
        "password": "testpassword",
        "name": "Test User"
    }

    response = test_client.post("/user", json=user_data)
    
    response = test_client.post("/user", json=user_data)
    
    assert response.status_code == 409
    
def test_login_user(test_client):
    user_data = {
        "name": "test_login",
        "email": "test_login@email.com",
        "password": "testpassword",
    }
    
    test_client.post("/user", json=user_data)

    response = test_client.post("/auth/login", json=user_data)
    
    assert response.status_code == 200