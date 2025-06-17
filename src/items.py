from dataclasses import dataclass


# Each item is a password a user has saved
# It holds the name of the item itself
# The username associated to the password and the password
@dataclass()
class Item:
    id: int
    user_id: int
    item_name: str
    username: str
    password: str
