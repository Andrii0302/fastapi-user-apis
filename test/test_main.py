import pytest
from main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)
def test_return_health_chek():
    response = client.get('/healthy')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status":"healthy"}
    