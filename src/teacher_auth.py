import hashlib
import hmac
import json
import secrets
from pathlib import Path


TEACHERS_FILE = Path(__file__).with_name("teachers.json")
PBKDF2_ITERATIONS = 600_000


def hash_password(password: str) -> dict[str, str]:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return {"salt": salt.hex(), "password_hash": password_hash.hex()}


def verify_password(password: str, credential: dict[str, str]) -> bool:
    try:
        salt = bytes.fromhex(credential["salt"])
        expected_hash = bytes.fromhex(credential["password_hash"])
    except (KeyError, TypeError, ValueError):
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return hmac.compare_digest(actual_hash, expected_hash)


def load_teacher_credentials(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}

    with path.open(encoding="utf-8") as credentials_file:
        data = json.load(credentials_file)

    teachers = data.get("teachers") if isinstance(data, dict) else None
    if not isinstance(teachers, list):
        raise ValueError("Teacher credentials must contain a teachers list")

    credentials = {}
    for teacher in teachers:
        if not isinstance(teacher, dict) or not all(
            isinstance(teacher.get(field), str)
            for field in ("username", "salt", "password_hash")
        ):
            raise ValueError("Each teacher needs a username and password hash")
        if teacher["username"] in credentials:
            raise ValueError(f"Duplicate teacher username: {teacher['username']}")
        credentials[teacher["username"]] = teacher

    return credentials