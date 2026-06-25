from locust import HttpUser, between

class BaseUser(HttpUser):
    abstract = True
    wait_time = between(1, 3)

def on_start(self):

    pass

def on_stop(self):

    pass