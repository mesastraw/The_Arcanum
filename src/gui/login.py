# This file contains file contains all components related to the login process of the UI
# Included:
# Login page
# New User page

# TODO: Add some password and username checks

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Input, Label, Button, Footer
from textual.screen import Screen
from utils import convert_to_int
from gui.app_state import db
from gui.main_page import MainPage
from textual.binding import Binding


class LoginPage(Screen):
    ''' The login page of our app the user will enter username and password
    There will be a button to create a new user and a button to log in
    '''

    CSS_PATH = "../assets/login_page.tcss"

    valid_user = vars(bool)

    def compose(self) -> ComposeResult:
        yield Footer()

        yield Container(

            Vertical(
                Label("Log In", id="login_title"),
                Input(
                    placeholder="Username", id="username_input_login"
                ),

                Horizontal(
                    Input(placeholder="Password",
                          id="password_input_login", password=True),

                    Button("👁", id="show_password_button_login"),
                ),

                # This will be invalid password or label
                Label("", id="login_label"),

                Horizontal(
                    Button("Log In", id="log_in_button"),
                    Button("Create New User", id="new_user_button"),
                    id="login_page_button_row"
                ),

                id="login_detials_coloumn"
            ),

            id="login_page_container",
        )

    # Whenever any button is pressed in the app
    def on_button_pressed(self, event: Button.Pressed) -> None:

        # Check if the button that was clicked is the log in button
        match event.button.id:
            case "log_in_button":
                self.handle_login()
            case "new_user_button":
                # Push the new user page on the stack
                # We will return to log in page after once the new user is created
                self.app.push_screen(NewUserPage())
            case "show_password_button_login":
                # Current hidden state
                password_status = self.query_one(
                    "#password_input_login", Input).password

                # if the password is already hidden show it if not hide it
                if password_status:

                    # Show the password
                    self.query_one("#password_input_login",
                                   Input).password = False
                    self.refresh()
                else:
                    # Hide the password
                    self.query_one("#password_input_login",
                                   Input).password = True
                    self.refresh()

    def handle_login(self):
        '''This function handles all  related to logging in the user'''

        username = self.query_one(
            "#username_input_login", Input).value.strip()
        password = self.query_one(
            "#password_input_login", Input).value.strip()

        # Checks if the user exists or has the correct password
        if self.validate_user(username, password):
            # Go to the main screen
            self.app.switch_screen(MainPage())

        else:
            # Erase the password field
            self.query_one(
                "#password_input_login", Input).value = ""

            self.query_one("#login_label", Label).update(
                "Incorrect username or password")

    def validate_user(self, username: str, password: str) -> bool:
        '''This function validates a user given a password and user name
        It will return true if the user is valid and false if not'''

        global logged_in_user_id

        # If the user is found in the database
        if db.is_user_exists(username):
            id = db.get_user_id(username)

            # Handle the int|None object
            id = convert_to_int(id)
            if id == 0:
                return False

            # The password of the user we got from the database
            pass_from_db = db.get_password(id)

            # Check if the passwords are equal
            if password == pass_from_db:
                self.app.logged_in_user_id = id
                return True

        return False


# The page where a user can create a new user account
class NewUserPage(Screen):

    CSS_PATH = "../assets/new_user_page.tcss"

    # Layout of the ui and its componenets
    def compose(self) -> ComposeResult:
        yield Footer()

        yield Container(
            Vertical(
                Label("Create New User", id="new_userpage_label"),
                Input(placeholder="username", id="new_userpage_username_input"),
                Horizontal(
                    Input(placeholder="password", password=True,
                          id="new_userpage_password_input"),

                    Button("👁", id="show_password_button_new_user_page"),
                ),

                Label("", id="user_creation_message"),

                Horizontal(
                    Button("Create", id="create_button"),
                    Button("Return", id="return_button"),
                    id="button_row",
                ),

                id="new_user_page_column"
            ),

            id="new_user_page_container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:

        match event.button.id:
            case "create_button":
                self.handle_user_creation()
            case "return_button":
                self.app.pop_screen()
            case "show_password_button_new_user_page":
                password_status = self.query_one(
                    "#new_userpage_password_input", Input).password

                # If the password is already hidden show it
                if password_status:
                    self.query_one("#new_userpage_password_input",
                                   Input).password = False
                else:
                    self.query_one("#new_userpage_password_input",
                                   Input).password = True

    def handle_user_creation(self):
        '''This function will get the inputs from the user and handle the process of creating a user'''

        username = self.query_one(
            "#new_userpage_username_input", Input).value.strip()
        password = self.query_one(
            "#new_userpage_password_input", Input).value.strip()

        # Check that the input fields aren't empty
        if username == "" or password == "":
            self.query_one("#user_creation_message", Label).update(
                "You must enter a username AND password!")
            return

        # A password must be 6 characters or more
        if not len(password) >= 6:
            self.query_one("#user_creation_message", Label).update(
                "password has to be 6 charecters or more")
            return
        else:
            self.query_one("#user_creation_message", Label).update("")

        # Check if the account already exists
        # if it does tell the user it exists
        if db.is_user_exists(username):
            self.query_one("#user_creation_message", Label).update(
                "User already exists")
        else:
            # Create the user and add them to the database
            db.add_user(username, password)
            self.app.pop_screen()
            # This comment stops a weird saving bug with my editor
