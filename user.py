from google.cloud import datastore
import hashlib
import os


class userCreds:
    def __init__(self, username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

def generate_creds(username, password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password_hash = hash_password(password, salt)
    return userCreds(username, password_hash, salt)

def hash_password(password, salt):
    encoded = password.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)

class userStore:
    def __init__(self, datastore_client):
        self.ds = datastore_client
    
    def verify_password(self, username, password):
        user_key = self.ds.key("userCreds", username)
        user = self.ds.get(user_key)
        if not user:
            return None
        hash_attempt = hash_password(password, user["salt"])
        if hash_attempt != user["password_hash"]:
            return None
        return userCreds(user["username"], user["password_hash"], user["salt"])
    
    def store_new_credentials(self, creds):
        user_key = self.ds.key("userCreds", creds.username)
        user = datastore.Entity(key=user_key)
        user["username"] = creds.username
        user["password_hash"] = creds.password_hash
        user["salt"] = creds.salt
        self.ds.put(user)

    def list_existing_users(self, txn=None):
        query = self.ds.query(kind="userCreds")
        users = query.fetch()
        return [u["username"] for u in users if "username" in u]