#!/usr/bin/env python3
import secrets
from os import path

CONFIG_PATH = "config.py"

write = True
if path.exists(CONFIG_PATH):
    answer = ""
    while True: 
        answer = input(f"{CONFIG_PATH} already exists. Do you want to use or overwrite it? [u/o]: ")
        answer = answer.strip().lower()
        if answer in ("u", "use"):
            write = False
            break
        elif answer in ("o", "overwrite"):
            break

if write:
    with open("config.py", "w") as f:
        f.write(f'SECRET_KEY = "{secrets.token_hex()}"\n\n')
        print("DATABASE INFO:")
        f.write(f'HOST = "{input("HOST (leave empty for UNIX socket): ")}"\n')
        f.write(f'DATABASE = "{input("DATABASE: ")}"\n')
        f.write(f'USER = "{input("USER: ")}"\n')
        f.write(f'PASSWORD = "{input("PASSWORD: ")}"\n')

from db import DB
DB().init()
