import json
# Imports the Google Cloud client library
from auth import get_user
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
    group["max_size"] = int(max_size)    
    group["owner"] = username

    # Saves the entity
    datastore_client.put(group)
    join_group(group_name, username, password)
    return True


def join_group(group_name, username, password):
    # Have to check if the group actually exists and if the user is allowed to join
    inGroup = False
    query = datastore_client.query(kind="Groups")
    query.add_filter("group_name", "=", group_name)
    groups = list(query.fetch())
    if str(password) == "None":
        pWord = ''
    else:
        pWord = password    
    if pWord == groups[0]["password"]:  
        print("Got password")         
        if (groups[0]["max_size"] > groups[0]["group_size"]):
            members = get_members_of_group(group_name)
            for member in members:
                if member["username"] == username:
                    inGroup = True
                    break 
            if(not inGroup):
                print("Good group size")
                # The Cloud Datastore key for the new entity
                kind = "Group_Members"
                group_key = datastore_client.key(kind)

                # Prepares the new entity
                group_mem = datastore.Entity(key=group_key)
                # Put attrubutes from the group in this spot
                group_mem["group_name"] = group_name
                group_mem["username"] = username
                
                # Saves the entity
                datastore_client.put(group_mem)
                
                groupKey = datastore_client.key("Groups", group_name)
                groups = datastore_client.get(groupKey)

                groups["group_size"] += 1

                datastore_client.put(groups)
            else:#failed because already in group
                print("Already in group")
        else:  #failed to join because of group size
            print("Failed to Join: Group size error")
    else:#failed because of incorrect password
        print("Failed to Join: Incorrect password")
    return
        

# returns an entity from datastore
def get_members_of_group(group_name):
    query = datastore_client.query(kind="Group_Members")
    query.add_filter("group_name", "=", group_name)
    group_members = list(query.fetch())   #retrieves and puts entities in a list 
    if not group_members:
        print("empty list")
        #need to handle this
        return 
    else:
        return group_members

# Pass in list of entities
def get_data_of_members(group_name):
    group_members = get_members_of_group(group_name)
    members_list = []
    for members in group_members:
        query = datastore_client.query(kind="userCreds")
        query.add_filter("username", "=", members["username"])        
        newMem = list(query.fetch())   #retrieves and puts entities in a list
        members_list.append(newMem[0])        
    return members_list


def get_groups_user_is_in(username):
    query = datastore_client.query(kind="Group_Members")
    query.add_filter("username", "=", username)
    groups = list(query.fetch())
    groupNames = list()    
    for name in groups:
        groupNames.append(name["group_name"])
    return groupNames
