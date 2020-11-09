import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Database:
    def __init__(self):
        # Using default service account tied to the GCP project
        firebase_admin.initialize_app()

        self.db = firestore.client()

    # Accessors

    # Reddit credentials
    def reddit_cred(self):
        return self.db.collection("reddit").document("reddit").get().to_dict()

    # All basic metadata
    def info(self):
        doc = self.db.collection("info").document("info").get().to_dict()

        subreddit = doc["subreddit"]

        # Adding word boundries, and combining regex
        trigger_list = "|".join([r"\b" + trigger + r"\b" for trigger in doc["trigger"]])

        # Replacing literals (quotes and new lines)

        script = doc["script"]

        for lang in script:
            script[lang] = script[lang].replace(r"\"", "\"")

        footer = doc["footer"].replace(r"\n", "\n").replace(r"\"", "\"")

        return (subreddit, trigger_list, script, footer)

    # List of cache
    def cache_list(self):
        return [cache.id for cache in self.db.collection("cache").stream()]

    # Mutator

    # Log to database
    def log(self, data):
        self.db.collection("logs").add(data)

    # Add to cache
    def add_cache(self, sub_id):
        self.db.collection("cache").document(sub_id).set({})