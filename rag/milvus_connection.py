from pymilvus import MilvusClient

import util.config_util


class MilvusConnection:
    _instance = None

    def __init__(self):
        self.client = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MilvusConnection, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance

    def get_client(self):
        if self.client is None:
            self.client =MilvusClient(uri=util.config_util.get_milvus_url(),token=util.config_util.get_milvus_token())
        return self.client


    def close_client(self):
        if self.client is not None:
            self.client.close()



