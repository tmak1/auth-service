def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_register_user(client):
    response = client.post('/register', json={
        "username": "testuser",
        "password": "password123",
        "role": "user"
    })
    assert response.status_code == 201
    assert b"User created" in response.data

def test_login_success(client):
    # Register first
    client.post('/register', json={"username": "loginuser", "password": "pw", "role": "user"})
    
    # Try login
    response = client.post('/login', json={
        "username": "loginuser",
        "password": "pw"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_login_failure(client):
    response = client.post('/login', json={
        "username": "nonexistent",
        "password": "wrong"
    })
    assert response.status_code == 401