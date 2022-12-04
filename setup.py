import secrets

with open("secret_config.py", "w") as f:
    f.write(f'SECRET_KEY = "{secrets.token_hex()}"')
