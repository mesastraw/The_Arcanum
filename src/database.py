# This file will hold all database methods for easy access and mutation of data
# In the next few lines all the methods that the database will need to implement will be outlined
# The database should be able to smoothly handle errors
#
# Features outlined:
# 1 - add_user method (Added)
#   ^ This method allows for easy addition of new users to the database this method
#   ^ should take a user_name and password and add them to the database
#
# 2 - get_username (Added)
#   ^ This function will take a user id and return the username of that user
#
# 3 - get_password (Added)
#   ^ This method will take a id and then return the password or an error
#
# 4 - delete_user (Added)
#   ^ This function will take a id and delete a user
#
# 5 - get_user_id (Added)
#   ^ This function will take a user_name and return the id of the user
#
# 6 -  add_item (Added)
#   ^ This method will take a user_id, item_name, username, password and added it to the database
#   ^ and relate it to the user_id passed in
#
# 7 - delete_item (Added)
#   ^ This will take an item id and delete that Item from the database
#   ^ When a user is deleted all their items will be deleted with them
#     ^ (This is default behavior from sqlite based on the tables we defined)
#
# 8 - get_all_items (Added)
#   ^ This is an inefficient function but exists to allow us to do something
#   ^ Takes a user id and returns all the tasks relating to that user
#
# 8 - is_user_exists (Added)
#   ^ This function will return true if the user is found false if the user doesnt exists
#

import sqlite3
from encrypt import decrpyt, encrypt
from items import Item
import os

# Location of our database file
DATABASE_FILE = "./data/userData.sqlite"
DIR_PATH = "./data/"


def check_data_directory():
    os.makedirs(DIR_PATH, exist_ok=True)


class Database:

    # Connects and sets up our database
    def __init__(self):
        # Connects to our database creates the file if it doesn't exist
        try:
            check_data_directory()
            # Update this so it checks that the data directory exists
            # Or setup some build system
            self.conn = sqlite3.connect(DATABASE_FILE)

        except sqlite3.Error as e:
            print("Database Error: ", e)

        cursor = self.conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        # Create the users table
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
                """)

        # Create the items table, with a foreign key to users
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    item_name TEXT NOT NULL,
                    username TEXT,
                    password TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """)

        cursor.close()

    # Find a way to handle when a user exists
    # This will add a user to the database
    def add_user(self, user_name: str, password: str):
        '''
        This function adds a new user to the database
        This function automatically encrypts the users password
        '''
        # Our insert Statement to add users
        sql_statment = ''' INSERT INTO users(user_name, password)
                            VALUES(?,?)'''

        # Create cursor
        cursor = self.conn.cursor()

        try:
            # Execute the INSERT statement
            cursor.execute(
                sql_statment, (user_name, encrypt(password)))

            self.conn.commit()
        except sqlite3.Error as e:
            cursor.close()
            print(f"Error adding user: {e}")

        finally:
            cursor.close()

        # Commit the changes
        self.conn.commit()
        cursor.close()

    def is_user_exists(self, username: str) -> bool:
        '''
        This function will take a username
        returns true if user exists
        false if not
        '''
        cursor = self.conn.cursor()

        sql_statement = '''
        SELECT COUNT(*) FROM users WHERE user_name=?
        '''

        cursor.execute(sql_statement, (username,))

        user_exists = cursor.fetchone()[0] > 0

        if user_exists:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

    # This function takes a user id and looks for the username
    # In the database
    def get_username(self, id: int):

        sql_statement = '''SELECT user_name
            From users
            WHERE id=?
            '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql_statement, (id,))

            result = cursor.fetchone()

            if result is None:
                cursor.close()
                return None

            cursor.close()
            return result[0]

        except sqlite3.Error as e:
            cursor.close()
            print(f"Database error: {e}")
            return None

    # Function makes it easy to get the password of a user that already exists

    def get_password(self, id: int):
        '''
        This function allows us to easily get the users password
        pass the username and it will automatically decrypt the users password and return it
        '''
        # SELECT statement
        sql_statment = ''' SELECT password
                            From users
                            WHERE id=? '''

        # Create a cursor
        cursor = self.conn.cursor()

        # Execute the command
        try:
            cursor.execute(sql_statment, (id,))

            result = cursor.fetchone()

            # Something with future error checking?
            if result is None:
                cursor.close()
                return None

            return decrpyt(result[0])

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

        finally:
            cursor.close()

    # This function given an id will delete that user
    def delete_user(self, id: int):
        cursor = self.conn.cursor()

        sql_statemenet = '''DELETE FROM users WHERE id = ? '''

        try:
            cursor.execute(sql_statemenet, (id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    # This function given a username will get the id of that user
    def get_user_id(self, user_name: str) -> int | None:
        cursor = self.conn.cursor()

        sql_statement = '''SELECT id
        FROM users
        WHERE user_name = ?
        '''

        try:
            cursor.execute(sql_statement, (user_name,))

            result = cursor.fetchone()

            if result is None:
                cursor.close()
                return None

            cursor.close()
            return result[0]

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    # The password and user name here aren't for the user account but for the account
    # The user saving to this item. The password here should also be encrypted
    def add_item(self, user_id: int, item_name: str, username: str, password: str):
        '''This function takes the user_id of the logged in user an item name,
        username and password the password is encrypted'''
        cursor = self.conn.cursor()

        sql_statemenet = '''INSERT INTO items(user_id, item_name, username, password)
        VALUES(?, ?, ?, ?)
        '''

        try:
            cursor.execute(
                sql_statemenet, (user_id, item_name, username, encrypt(password)))
            self.conn.commit()
            cursor.close()

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

        cursor.close()

    def delete_item(self, item_id):
        cursor = self.conn.cursor()

        sql_statemnt = '''
        DELETE FROM items 
        WHERE id=?
        '''

        try:
            cursor.execute(sql_statemnt, (item_id,))
            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    # This is inefficient but exists to allow us to do something
    # Instead of nothing
    # Takes a user id and returns all the tasks relating to that user
    def get_all_items(self, user_id):
        '''This function takes the id of the user
        It returns all rows linked to the user in the items table
        It does NOT decrypt the passwords that are saved
        '''

        sql_statement = '''
        SELECT * FROM items
        WHERE user_id=?
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql_statement, (user_id,))

            result = cursor.fetchall()

            item_list = []

            for item in result:
                item_list.append(Item(*item))

            return item_list

        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    def get_all_items_names(self, user_id: int):
        '''This function takes a user id and returns
        the names of all the items linked to that user'''

        sql_statement = '''
        SELECT item_name FROM items
        WHERE user_id=?
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql_statement, (user_id,))

            result = cursor.fetchall()

            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    def get_item_id(self, item_name: str):
        sql_statement = '''
        SELECT id FROM items
        WHERE item_name=?
        '''
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql_statement, (item_name,))
            result = cursor.fetchone()

            return result[0]
        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    def get_item_details(self, item_id: int):
        '''This function gets the item_name, username and password
        It decrypts the password (This returns a tuple)'''

        print(f"Item id: {item_id}")

        sql_statement = '''
        SELECT 
            item_name,
            username,
            password
        FROM items
        WHERE
            id=?
        '''

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql_statement, (item_id,))
            result = cursor.fetchone()

            print(f"Item detials: {result}")

            item_name = result[0]
            username = result[1]
            password = decrpyt(result[2])

            return (item_name, username, password)
        except sqlite3.Error as e:
            print(f"Database error: {e}")

        finally:
            cursor.close()

    # This functions only purpose for debugging the database
    def debug_user(self):
        '''
        This function is purely for debugging
        '''

        sql_statment = ''' SELECT * FROM users'''

        # Create a cursor
        cursor = self.conn.cursor()

        # Execute the SELECT statement
        cursor.execute(sql_statment)

        # Returns a list of a tuple of each row
        rows = cursor.fetchall()

        for row in rows:
            print(row)
