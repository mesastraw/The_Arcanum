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
        self.container = Container(id="content_container")

        # If create_new_user show new user page
        # If show contents of item show the contents
        # use refresh function to redraw
        yield Label("Item Content")
        yield self.container

    # This function watches our reactive variable
    # Its called every time our variable is mutated
    def watch_template_chosen(self, old_value, new_value):
        self.update_display()

    # Updates our container so it can show the widget we need
    def update_display(self):
        self.refresh_folder_list()

        # Erase all the currently displayed widgets
        self.container.remove_children()

        match self.template_chosen:
            case 0:
                self.container.remove_children()
            case 1:
                self.container.mount(ShowItemDetails())
            case 2:
                self.container.mount(CreatNewItemScreen())

    # This function is called every time the displayed item needs to be updated
    def update_item_details(self, new_id: int):
        self.template_chosen = 1

        # Update the id of the item shown
        item_details = self.query_one(ShowItemDetails)
        item_details.item_id = new_id

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
        yield Container(
            Vertical(
                Input(placeholder="name", id="name_input_create_item"),
                Input(placeholder="username", id="username_input_create_item"),

                Horizontal(
                    Input(placeholder="password",
                          password=True, id="password_input_create_item"),
                    Button(label="👁  ",
                           id="show_password_button_create_item")
                ),
                Label("", id="info_for_user_label"),



                id="form_container_create_item"
            ),

            Horizontal(
                Button(label="Save", id="save_button_create_item"),
                Button(label="Cancel", id="cancel_button_create_item"),
                id="button_row_create_item"
            ),

            id="new_item_container_create_item"
        )

    # Called whenever any of the buttons are pressed
    def on_button_pressed(self, event: Button.Pressed) -> None:

        # Match the button pressed
        # To its logic
        match event.button.id:
            case "show_password_button_create_item":

                # If password is hidden unhide it and vice versa
                if self.query_one(
                        "#password_input_create_item", Input).password:
                    self.query_one(
                        "#password_input_create_item", Input).password = False
                else:
                    self.query_one(
                        "#password_input_create_item", Input).password = True

            case "save_button_create_item":
                self.save_button_logic()
                # Access out ItemView widget
                self.parent.parent.template_chosen = 0
                self.parent.parent.update_display()
                self.parent.parent.refresh_folder_list()

            case "cancel_button_create_item":
                self.cancel_button_logic()

            case _:
                pass

    def save_button_logic(self):
        '''This function handles getting the inputted name, username and password and saving it to the database'''

        item_name = self.query_one(
            "#name_input_create_item", Input).value.strip()

        username = self.query_one(
            "#username_input_create_item", Input).value.strip()

        password = self.query_one(
            "#password_input_create_item", Input).value.strip()

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

    def cancel_button_logic(self):
        # Reset all the values to zero
        self.query_one(
            "#name_input_create_item", Input).value.strip()

        self.query_one(
            "#username_input_create_item", Input).value.strip()

        self.query_one(
            "#password_input_create_item", Input).value.strip()

        # Change the template to none template
        self.parent.parent.template_chosen = 0
        self.parent.parent.update_display()


# This is the screen shown whenever a
# Item is selected to show its details
class ShowItemDetails(VerticalScroll):
    '''Widget that's show to display the details of a selected item'''

    item_id = reactive(1)
    is_mounted = False
    show_password = False

    def compose(self) -> ComposeResult:
        self.show_password = False

        yield Container(
            Label("Name: ", id="name_label_details"),
            Label("Username: ", id="username_label_details"),
            # Set this up eventually to use the show password button
            Horizontal(
                # Set it up where the label will show the password after the button is clicked
                Label("Password: ", id="password_label_details"),
                Button("👁", id="show_password_button_details"),

                id="password_item_view_box_details",
            ),

            id="item_details_wrapper"
        )

        yield Horizontal(
            Button("Edit", id="edit_button"),
            Button("🗑", id="delete_button"),
            id="item_detail_action_buttons",
        )

    def on_mount(self) -> None:
        self.is_mounted = True
        self.show_password = False
        self.get_item_details()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "edit_button":
                # Not implemented yet
                print("Not implemented yet")

            case "delete_button":
                self.delete_logic()

            case "show_password_button_details":
                # If the password is already shown hide it
                if not self.show_password:
                    self.show_password = True
                else:
                    self.show_password = False

                self.get_item_details()

    # Called whenever the item_id variable is updated
    def watch_item_id(self, old_val, new_val):
        self.show_password = False
        if not self.is_mounted:
            print("Not mounted")
            return

        self.get_item_details()

    def delete_logic(self):
        print(f"item: {self.item_id}")
        db.delete_item(self.item_id)

        self.parent.parent.template_chosen = 0
        self.parent.parent.update_display()

    def get_item_details(self):
        # Updates the values of name. Username and password
        name, username, password = db.get_item_details(self.item_id)

        self.query_one("#name_label_details").update(f"Name: {name}")
        self.query_one("#username_label_details", Label).update(
            f"Username: {username}")

        if not self.show_password:
            password = len(password) * "."

        self.query_one("#password_label_details", Label).update(
            f"Password: {password}")


# This class is for the screen shown when editing a item
class EditItemDetails(Vertical):

    def compose(self):
        return
