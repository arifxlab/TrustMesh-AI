from app.security import password_security


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
