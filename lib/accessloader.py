import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path)

allowed_users_string = os.getenv("ALLOWED_USERS")
ALLOWED_USERS = allowed_users_string.split(",") if allowed_users_string else []

if ALLOWED_USERS:
    print(f"⚠️ Dangerous Access List:")
    for idx, user_id in enumerate(ALLOWED_USERS, 1):
        print(f"    {idx}: {user_id}")
else:
    print("🔒 No authorized users found.")

def is_authorized(user_id: str) -> bool:
    return user_id in ALLOWED_USERS
