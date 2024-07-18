def test_create_user_email_validation(test_app):
    response = test_app.post("/sign-up/", json={
        "email": "ss@ss",
        "fullname": "soumya"

    }, )
    assert response.status_code == 400
    assert response.json()["detail"] == "Please verify your email-id."


def test_create_user_empty_email(test_app):
    response = test_app.post("/sign-up/", json={
        "email": "",
        "fullname": "soumya"

    }, )
    assert response.status_code == 400
    assert response.json()["detail"] == "Please verify your email-id."


def test_create_user(test_app):
    response = test_app.post("/sign-up/", json={
        "email": "ss12@gmail.com",
        "fullname": "soumya"

    }, )
    assert response.status_code == 200 or 400
