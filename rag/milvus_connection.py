import sys

from pymilvus import MilvusClient

from util import file_util, config_util, global_varb

"""如果需要在flask的生命周期中使用这个client，只需要在g中获取实例， 如果没有获取成功， 重新实例后存储即可"""
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
            self.client =MilvusClient(uri=config_util.get_milvus_url(),token=config_util.get_milvus_token())
        return self.client


    def close_client(self):
        if self.client is not None:
            self.client.close()

    """现在还没有想好怎么管理connection，先按照/data/prd/{connection}来区分好了"""
    def get_connection(self, connection_name=None):
        if connection_name:
            self._check_and_create_connection(connection_name)
        else:
            #TODO: 要不要全局建立链接？先就一个吧
            raise ValueError("connection_name is required")

    def _check_and_create_connection(self, connection_name):
        if not self.client.has_connection(connection_name):
            self.client.create_collection(
                collection_name=connection_name,
                dimension=384,  # 使用 Sentence Transformer 的维度
                auto_id=True
            )

    @staticmethod
    def get_connection_list():
        project_root = file_util.get_abs_path(sys.argv[0]).split(global_varb.project_root)[0]
        root = project_root+global_varb.project_root+global_varb.prd_storage
        prd_paths = file_util.get_all_sub_path(root)
        return [prd_name.split(global_varb.prd_storage)[1].split("/")[1].strip("/") for prd_name in prd_paths ]


if __name__ == "__main__":
    print(MilvusConnection.get_connection_list())


