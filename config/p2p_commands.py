from http import client
from config.p2p_funcs import download, upload

server_commands = {
    "DOWNLOAD": lambda conn, filename, file_type: upload(conn, filename, file_type),
    "UPLOAD": lambda conn, filename, file_type: download(conn, filename, file_type)
}

client_commands = {
    "DOWNLOAD": lambda conn, filename, file_type: download(conn, filename, file_type),
    "UPLOAD": lambda conn, filename, file_type: upload(conn, filename, file_type)
}