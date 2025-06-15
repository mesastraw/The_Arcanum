from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll, Container, Vertical
from textual.reactive import reactive
from textual.widgets import Input, Label, Button, Static
from gui.app_state import db


# Shows the contents of a selected item
class ItemView(VerticalScroll):
    '''This widget handles all the logic for show the details for
    selected items and creating new items'''

    # 0 for show nothing
    # 1 for show item details
    # 2 for create new item
    template_chosen = reactive(0)

    def compose(self):
        # If create_new_user show new user page
        # If show contents of item show the contents
        # use refresh function to redraw
        yield Label("Item Content")
        yield Container(id="content_container")

    # This function watches our reactive variable
    # Its called every time our variable is mutated
    def watch_template_chosen(self, old_value, new_value):
        self.update_display()

    # Updates our container so it can show the widget we need
    def update_display(self):
        container = self.query_one("#content_container", Container)

        # Erase all the currently displayed widgets
        container.remove_children()

        match self.template_chosen:
            case 0:
                container.remove_children()
            case 1:
                container.mount(ShowItemDetails())
            case 2:
                container.mount(CreatNewItemScreen())

    # This function is called every time the displayed item needs to be updated
    def update_item_details(self, item_id: int):
        self.template_chosen = 1

        # Update the id of the item shown
        item_details = self.query_one(ShowItemDetails)
        item_details.item_id = item_id

        # Refresh so changes can be shown
        item_details.refresh()

    def refresh_folder_list(self):
        # Access main page widget
        self.parent.parent.refresh_item_list()


# This is the screen displayed whenever the
# create new Item button is clicked
class CreatNewItemScreen(Vertical):
    '''Widget that's shown to create a new item'''

    def compose(self) -> ComposeResult:
        # The input field
        yield Vertical(
            Input(placeholder="name", id="name_input"),
            Input(placeholder="username", id="username_input"),

            Horizontal(
                Input(placeholder="password",
                      password=True, id="password_input"),
                Button(label="show Password", id="show_password_button")
            ),
            Label("", id="info_for_user_label"),

            Static(id="spacer"),

            Horizontal(
                Button(label="Save", id="save_button"),
                Button(label="Cancel", id="cancel_button"),
                id="button_row"
            ),

            id="form_container"
        )

    # Called whenever any of the buttons are pressed
    def on_button_pressed(self, event: Button.Pressed) -> None:

        # Match the button pressed
        # To its logic
        match event.button.id:
            case "show_password_button":
                print("show password")

            case "save_button":
                self.save_button_logic()
                # Access out ItemView widget
                self.parent.parent.template_chosen = 0
                self.parent.parent.update_display()
                self.parent.parent.refresh_folder_list()

            case "cancel_button":
                print("Cancel button")

            case _:
                pass

    def save_button_logic(self):
        '''This function handles getting the inputted name, username and password and saving it to the database'''

        item_name = self.query_one("#name_input", Input).value.strip()
        username = self.query_one("#username_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        label = self.query_one("#info_for_user_label", Label)

        # Check if any of the fields are empty
        if item_name == "" or username == "" or password == "":
            label.update("You must enter a name, username and password!")
            return

        print(f"Item: {item_name}")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Label: {label}")

        # Finally add the item to the database
        db.add_item(self.app.logged_in_user_id, item_name, username, password)


# This is the screen shown whenever a
# Item is selected to show its details
class ShowItemDetails(VerticalScroll):
    '''Widget that's show to display the details of a selected item'''

    item_id = reactive(0)

    def compose(self) -> ComposeResult:
        yield Label("Name: ", id="name_label_items")
        yield Label("Username: ", id="username_label")

        # Set this up eventually to use the show password button
        yield Horizontal(
            # Set it up where the label will show the password after the button is clicked
            Label("Password: ", id="password_label"), Button(
                "Show password", id="show_password_button")
        )

        yield Button("Edit", id="edit_button")

    def on_mount(self) -> None:
        self.get_item_details()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "edit_button":
                print("Todo!")

    def get_item_details(self):
        "Updates the values of name. Username and password"
        name, username, password = db.get_item_details(self.item_id)

        self.query_one("#name_label_items", Label).update(f"Name: {name}")
        self.query_one("#username_label", Label).update(
            f"Username: {username}")
        self.query_one("#password_label", Label).update(
            f"Password: {password}")


# This class is for the screen shown when editing a item
class EditItemDetails(Vertical):
    print("Todo!")
