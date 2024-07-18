def test_authentication_wrong_email(test_app):
    response = test_app.post("/sign-in/", json={
        "email": "randomemail",
        "password": "password"

    }, )
    assert response.status_code == 400
    assert response.json()["detail"] == "Entered email was not found."


def test_authentication_without_activation(test_app):
    response = test_app.post("/sign-in/", json={
        "email": "ss12@gmail.com",
        "password": "password"

    }, )
    assert response.status_code == 400
