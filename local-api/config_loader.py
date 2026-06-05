import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(
    BASE_DIR,
    "..",
    "configs",
    "chatbot_configs.json"
)


def load_configs():

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_client_config(client_id):

    configs = load_configs()

    return configs.get(client_id)



# import json


# def load_configs():

#     with open(
#         "../configs/chatbot_configs.json",
#         "r",
#         encoding="utf-8"
#     ) as f:

#         return json.load(f)


# def get_client_config(client_id):

#     configs = load_configs()

#     return configs.get(client_id)