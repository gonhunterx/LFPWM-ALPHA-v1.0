from app.users import User
from app.sql_db import create_connection, create_database
from app.home_page import home_page
import bcrypt

c, conn = create_connection()


def login():
    # ask for login info
    username = input("Enter username: ")
    password = input("Enter password: ")
    # check if the username and password match

    c.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user_login = c.fetchone()
    if user_login and bcrypt.checkpw(
        password.encode("utf-8"), user_login[1].encode("utf-8")
    ):
        user = User(username, password)
        home_page(user)
    else:
        print("Invalid input. Please try again or register.")


def register():
    print("Please create an account 😊")
    username = input("Username: ")
    password = input("Password: ")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    # check if username already exists
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        print("This user already exists please use another name.")
    else:
        # account does not exist and you can enter the information
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password.decode("utf-8")),
        )
        conn.commit()
        print("Registration successful!")


def main_menu():
    print(
        """
=======================
1. Login
2. Register
3. Exit
          """
    )
    choice = input("Input: ")
    return choice


def main():
    c, conn = create_connection()
    try:
        print("=======================")
        print("Welcome to LamaForge PW Manager")
        create_database()
        while True:
            login_menu_choice = main_menu()
            if login_menu_choice == "1":
                login()
            elif login_menu_choice == "2":
                register()
            elif login_menu_choice == "3":
                conn.close()  # Close the connection before exiting
                break
            else:
                print("Invalid input. Please input 1, 2, or 3.")
    finally:
        conn.close()  # Make sure to close the connection even if there's an error


if __name__ == "__main__":
    main()
