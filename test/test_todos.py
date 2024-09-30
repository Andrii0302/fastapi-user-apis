from routers.todos import get_db, get_current_user
from fastapi import status
from models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Test Todo', 'description': 'Test Description', 'id': 1,'priority': 1,'owner_id':1}]

def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Test Todo', 'description': 'Test Description', 'id': 1,'priority': 1,'owner_id':1}

def test_read_one_authenticated_not_found():
    response = client.get('/todos/todo/100')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

def test_create_todo(test_todo):
    request_data={
        'title': 'New Todo',
        'description': 'New Description',
        'priority': 5,
        'complete': False
    }
    response = client.post('/todos/todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db=TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False
    }
    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Updated Todo'

def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False
    }
    response = client.put('/todos/todo/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}