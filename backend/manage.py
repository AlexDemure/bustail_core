import os

# import modules used here -- sys is a very standard one
import sys

# Gather our code in a main() function
def main():
    command = sys.argv[1]
    app_name = sys.argv[2]

    if command == 'createapp':
        create_app(app_name)

    return 0


def create_app(app_name):
    files = [
        "__init__.py", "admin.py", "crud.py", "models.py",
        "routers.py", "schemas.py", "views.py"
    ]
    current_path = os.getcwd()

    app_path = f"{current_path}/{app_name}"
    if os.path.isdir(app_name):
        return 0

    os.mkdir(app_path)

    for file in files:
        with open(f"{app_path}/{file}", 'w') as f:
            pass


if __name__ == '__main__':
  main()
