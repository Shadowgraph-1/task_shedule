import secrets

def secret_key():
    key = secrets.token_hex(16)
    return key