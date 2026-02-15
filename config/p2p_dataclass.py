from dataclasses import dataclass
import json

def open_config(filename):

    with open(filename, "r") as f:
        data = json.load(f)
    
    return data

@dataclass
class BasicConfig:
    ufile_path: str # File path for files you want to send
    dfile_path: str # File path for files you want to recieve and store
    log_file: str

    buffer_size: int # Please do not change buffer size in json config file


@dataclass()
class ServerDataclass:
    host: str
    port: int

json_data = open_config("config/json_files/config.json")
server_dataclass = ServerDataclass(host=json_data["host"], port=json_data["port"])
basic_config = BasicConfig(ufile_path=json_data["file_paths"]["ufile_path"], dfile_path=json_data["file_paths"]["dfile_path"], log_file=json_data["file_paths"]["log_file"], buffer_size=json_data["buffer_size"])
