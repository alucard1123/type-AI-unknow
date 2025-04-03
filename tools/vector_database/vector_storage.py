# 这个工具是用来根据data文件夹中的文件插入到milvus数据库， 提供新的文件存储， 向量去重， 重建等数据的的存储功能。


"""存储新的data文件
input file: 文件名或者文件夹
"""
import util.file_util


def store_new(file):
    if util.file_util.is_folder(file):
        pass


def _store_single_file(rawdata:list):
