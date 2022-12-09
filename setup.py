import secrets

with open("config.py", "w") as f:
    f.write(f'SECRET_KEY = "{secrets.token_hex()}"\n\n')
    print("DATABASE INFO:")
    f.write(f'HOST = "{input("HOST: ")}"\n')
    f.write(f'DATABASE = "{input("DATABASE: ")}"\n')
    f.write(f'USER = "{input("USER: ")}"\n')
    f.write(f'PASSWORD = "{input("PASSWORD: ")}"\n')

import db
db.init()
