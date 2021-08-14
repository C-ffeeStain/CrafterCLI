import os
import toml

if not os.path.exists("settings.cfg"):
    with open("settings.cfg", "w") as f:
        settings = {
            "username": input("Enter your username: "),
            "password": input("Enter your password: ")
        }
        toml.dump(settings, f)

if __name__ == "__main__":
    print("Hello World")
