import configparser

#read config.ini and get config_name value
def get_configer(section, config_name):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.get(section, config_name)

def get_milvus_url():
    return (f"http://{get_configer('vector_database', 'host')}:"
            f"{get_configer('vector_database', 'port')}")

def get_milvus_token():
    return (f"{get_configer('vector_database', 'user_name')}:"
            f"{get_configer('vector_database', 'pass_word')}")