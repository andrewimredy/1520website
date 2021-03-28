# Imports the Google Cloud client library
from google.cloud import datastore
# Instantiates a client
datastore_client = datastore.Client()

class GroupInfo:
    """Container class for group info"""

    def __init__(self, group_name, password, group_size):
        self.group_name = group_name
        self.password = password
        self.group_size = group_size
        

def create_group(group_name, max_size, password, username):        
    # The kind for the new entity
    kind = "Groups"
    # The Cloud Datastore key for the new entity
    group_key = datastore_client.key(kind, group_name)

    # Prepares the new entity
    group = datastore.Entity(key=group_key)
    # Put attrubutes from the group in this spot
    group["group_name"] = group_name
    group["group_size"] = 0
    group["password"] = password
    group["max_size"] = max_size    
    group["owner"] = username

    # Saves the entity
    datastore_client.put(group)
    join_group(group_name,username)
    return True

def join_group(group_name, username):
    # Have to check if the group actually exists and if the user is allowed to join
    datastore_client
    # The Cloud Datastore key for the new entity
    group_key = datastore_client.key("Group_Members")

    # Prepares the new entity
    group_mem = datastore.Entity(key=group_key)
    # Put attrubutes from the group in this spot
    group_mem["group_name"] = group_name
    group_mem["username"] = username

    # Saves the entity
    datastore_client.put(group_mem)


