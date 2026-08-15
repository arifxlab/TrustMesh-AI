from datetime import timedelta

from app.security import password_security, token_security


def test_password_hash_is_not_plaintext() -> None:
    password = "CorrectHorseBatteryStaple123!"

    password_hash = password_security.hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2")


def test_password_verification_succeeds_for_correct_password() -> None:
    password = "CorrectHorseBatteryStaple123!"

    password_hash = password_security.hash_password(password)

    assert password_security.verify_password(password, password_hash) is True


def test_password_verification_fails_for_incorrect_password() -> None:
    password_hash = password_security.hash_password(
        "CorrectHorseBatteryStaple123!",
    )

    assert (
        password_security.verify_password(
            "WrongPassword123!",
            password_hash,
        )
        is False
    )


def test_same_password_produces_different_hashes() -> None:
    password = "CorrectHorseBatteryStaple123!"

    first_hash = password_security.hash_password(password)
    second_hash = password_security.hash_password(password)

    assert first_hash != second_hash


def test_access_token_contains_subject() -> None:
    token = token_security.create_access_token("user-123")

    payload = token_security.decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "user-123"


def test_access_token_contains_issued_at_and_expiration() -> None:
    token = token_security.create_access_token("user-123")

    payload = token_security.decode_access_token(token)

    assert payload is not None
    assert "iat" in payload
    assert "exp" in payload
    assert payload["exp"] > payload["iat"]


def test_expired_access_token_is_rejected() -> None:
    token = token_security.create_access_token(
        "user-123",
        expires_delta=timedelta(seconds=-1),
    )

    assert token_security.decode_access_token(token) is None


def test_tampered_access_token_is_rejected() -> None:
    token = token_security.create_access_token("user-123")

    header, payload, signature = token.split(".")
    tampered_payload = f"{payload[:-1]}{'a' if payload[-1] != 'a' else 'b'}"
    tampered_token = f"{header}.{tampered_payload}.{signature}"

    assert token_security.decode_access_token(tampered_token) is None


def test_access_token_with_wrong_secret_is_rejected() -> None:
    import jwt

    token = jwt.encode(
        {
            "sub": "user-123",
        },
        "wrong-secret-for-trustmesh-security-test-2026",
        algorithm="HS256",
    )

    assert token_security.decode_access_token(token) is None
