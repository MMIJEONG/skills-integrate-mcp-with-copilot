import getpass
import json
import os
import sys

from teacher_auth import TEACHERS_FILE, hash_password, load_teacher_credentials


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python create_teacher.py <username>")

    username = sys.argv[1].strip()
    if not username:
        raise SystemExit("Username cannot be empty")

    credentials = load_teacher_credentials(TEACHERS_FILE)
    if username in credentials:
        raise SystemExit("That teacher username already exists")

    password = getpass.getpass("New teacher password (minimum 12 characters): ")
    if len(password) < 12:
        raise SystemExit("Password must be at least 12 characters")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords do not match")

    credentials[username] = {"username": username, **hash_password(password)}
    TEACHERS_FILE.write_text(
        json.dumps({"teachers": list(credentials.values())}, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(TEACHERS_FILE, 0o600)
    print(f"Teacher {username!r} added. Restart the server to apply the change.")


if __name__ == "__main__":
    main()