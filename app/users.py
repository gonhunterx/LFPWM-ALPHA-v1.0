from app.sql_db import create_connection

c, conn = create_connection()


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def insert_data(self, title, data):
        c.execute(
            "INSERT INTO passwords (user_id, title, storage) VALUES ((SELECT id FROM users WHERE username = ?), ?, ?)",
            (self.username, title, data),
        )
        conn.commit()

    def view_data(self):
        c.execute(
            "SELECT title, storage FROM passwords WHERE user_id = (SELECT id FROM users WHERE username = ?)",
            (self.username,),
        )
        results = c.fetchall()
        if results:
            data_list = [(result[0], result[1]) for result in results if result[1]]
            if data_list:
                for index, (title, data) in enumerate(data_list, start=1):
                    print(f"{index}. {title}\n  - {data}")
            else:
                print("No saved data.")
        else:
            print("No saved data.")

    def delete_data(self, data_to_delete):
        c.execute(
            "DELETE FROM passwords WHERE user_id = (SELECT id FROM users WHERE username = ?) AND title = ?",
            (self.username, data_to_delete),
        )
        conn.commit()
