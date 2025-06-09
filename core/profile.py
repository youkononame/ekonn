import time
import core.mongo


class Profile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 500
        self.last_reward_claim = time.time()
        self.update()

    def update(self):
        core.mongo.collection.update_one({"user_id": self.user_id}, {"$set": vars(self)}, upsert=True)
        return self


def create_profile(document):
    profile = Profile(document["user_id"])
    profile.balance = document["balance"]
    profile.last_reward_claim = document["last_reward_claim"]
    profile.update()
    return profile
