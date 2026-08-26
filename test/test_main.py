import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
import models
from database import Base
from router import auth, transactions
from sqlalchemy.pool import StaticPool



SQLALCHEMY_DATABASE_URL = 'sqlite://'


test_engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread': False},poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=test_engine)






def override_get_db():
    db = TestingSessionLocal()
    try:

        yield db


    finally:


        db.close()




app.dependency_overrides[auth.get_db] = override_get_db
app.dependency_overrides[transactions.get_db] = override_get_db


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    return TestClient(app)




def create_user(client):



    response = client.post(
        '/auth/register',
        json={
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': '123456'
        }
    )





    assert response.status_code == 201





    response = client.post('/auth/login',data={'username': 'testuser','password': '123456'})





    assert response.status_code == 200




    token = response.json()['access_token']

    return {'Authorization': f'Bearer {token}'}








def create_transaction(client, headers):
    response = client.post(
        '/transactions',
        json={
            'title': 'Lunch',
            'amount': 250,
            'type': 'expense',
            'category': 'Food',
            'date': '2026-08-26'
        },
        headers=headers
    )

    assert response.status_code == 200

    return response.json()['id']






def test_create_transaction(client):

    headers = create_user(client)
    response = client.post(
        '/transactions',
        json={
            'title': 'Bus',
            'amount': 100,
            'type': 'expense',
            'category': 'Transport',
            'date': '2026-08-26'
        },
        headers=headers
    )




    assert response.status_code == 200
    response_data = response.json()

    assert response_data['title'] == 'Bus'
    assert response_data['amount'] == 100







def test_get_transaction(client):
    headers = create_user(client)

    create_transaction(client, headers)

    response = client.get('/transactions',headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1











def test_get_specific_transaction(client):

    headers = create_user(client)
    transaction_id = create_transaction(client, headers)
    response = client.get(f'/transactions/{transaction_id}',headers=headers)

    assert response.status_code == 200
    assert response.json()['id'] == transaction_id







def test_update_transaction(client):

    headers =create_user(client)
    transaction_id = create_transaction(client, headers)
    response = client.put(f'/transactions/{transaction_id}',
        json={'amount': 500,'category': 'Restaurant'},headers=headers)



    assert response.status_code == 200
    assert response.json()['amount'] == 500
    assert response.json()['category'] == 'Restaurant'







def test_delete_transaction(client):

    headers = create_user(client)
    transaction_id = create_transaction(client, headers)
    response = client.delete(f'/transactions/{transaction_id}',headers=headers)
    assert response.status_code == 200

    response = client.get(f'/transactions/{transaction_id}',headers=headers)
    assert response.status_code == 404