from dataclasses import dataclass


# This class represents an individual user
# Our users will be stored in the database
# To search for users we will just query for their username
@dataclass()
class User:
    id: int
    user_name: str
    password: str
