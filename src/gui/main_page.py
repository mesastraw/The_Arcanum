from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Label, Button, ListItem, ListView, Footer
from textual.screen import Screen
from textual.message import Message
from gui.app_state import db
from gui.items import ItemView


class FolderView(VerticalScroll):
    '''This widget holds all logic related to displaying the folders'''

    def compose(self) -> ComposeResult:
        yield Label("Folders go here")


# Shows the contents of a selected folder
class FolderContentView(VerticalScroll):
    '''This shows the contents of a selected folder'''

    # Our message for whenever an item is selected
    class Selected(Message):
        '''This message is sent whenever an item from the list is selected'''

        def __init__(self, item_id: int):
            print(f"The item id inside slected: {item_id}")
            self.item_id = item_id
            super().__init__()

    class CreateNewItem(Message):
        '''This message is sent whenever the create new item button is pressed'''

        def __init__(self):
            super().__init__()

    def __init__(self):
        print("Sending Message")
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Folder content")
        yield ListView(id="folder_content_list")
        yield Button(label="+", id="create_new_item")

    def on_mount(self):
        self.refresh_list()

    def refresh_list(self):
        '''This is a function that will refresh the list and should be
        called every time a new item is created or an item is deleted'''
        print("Refreshing list")
        list = self.query_one("#folder_content_list")
        list.clear()

        # Get all of our item names and turn them into a list item
        for item in db.get_all_items_names(self.app.logged_in_user_id):
            print(f"ITem: {item}")
            # Change this to where it only gets the names
            list.append(ListItem(Label(*item)))

    # Called whenever one of the list items is clicked
    def on_list_view_selected(self, event: ListView.Selected):
        '''
        This is called whenever an item from the list is selected
        '''

        # Gets the label that holds our selected item name

        label = event.item.query_one(Label)
        item_name = label.renderable

        # Get the id of the item from the database
        print(f"Item name: {item_name}")
        id = db.get_item_id(item_name)

        print(f"The collected item id: {id}")

        self.post_message(self.Selected(item_id=id))

    # Called Whenever a button is pressed in this widget
    def on_button_pressed(self, event: Button.Pressed):
        # Whenever the create new user button is pressed
        # Send the message to update the ItemView
        self.post_message(self.CreateNewItem())


# This is the screen where everything in this file is displayed
class MainPage(Screen):
    '''This is the screen for the main page of the app It connects
    all the other widgets it also handles all the messaging logic'''

    # self.app.logged_in_user_id

    CSS_PATH = ["../assets/new_user_page.tcss",
                "../assets/creat_new_item.tcss"]

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Horizontal(
            # FolderView(), Not enough time to implement this
            FolderContentView(),
            ItemView(),
        )

    # Whenever the show item details message is sent
    def on_folder_content_view_selected(self, message: FolderContentView.Selected) -> None:
        # Get our item view widget
        item_view = self.query_one(ItemView)

        # Call the update function
        id = message.item_id
        print(f"ID inside mina_page message receiver: {id}")
        item_view.update_item_details(id)

    # This function refreshes the list that shows the contents of a folder
    def refresh_item_list(self):
        print("MainPage redfreshlist")
        self.query_one(FolderContentView).refresh_list()

    # Whenever the create new message is sent out
    def on_folder_content_view_create_new_item(self, message: FolderContentView) -> None:
        item_view = self.query_one(ItemView)

        # Set the current template to the create new item template
        item_view.template_chosen = 2
        item_view.refresh()
