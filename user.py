from google.cloud import datastore

class userCreds:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def generate_creds(username, password):
    return userCreds(username, password)

class userStore:
    def __init__(self, datastore_client):
        self.ds = datastore_client
    
    def verify_password(self, username, password):
        user_key = self.ds.key("userCreds", username)
        user = self.ds.get(user_key)
        if not user:
            return None
        if password != user["password"]:
            return None
        return userCreds(user["username"], user["password"])
    
    def store_new_credentials(self, creds):
        user_key = self.ds.key("userCreds", creds.username)
        user = datastore.Entity(key=user_key)
        user["username"] = creds.username
        user["password"] = creds.password
        self.ds.put(user)

    def list_existing_users(self, txn=None):
        query = self.ds.query(kind="userCreds")
        users = query.fetch()
        return [u["username"] for u in users if "username" in u]