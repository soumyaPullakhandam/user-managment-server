def test_create_user_email_validation(test_app):
    response = test_app.post("/verify/", json={
        "email_token": "randomemailtoken",
        "password": "password"

    }, )
    assert response.status_code == 400
    assert response.json()["detail"] == "The confirmation link is invalid or has expired."

