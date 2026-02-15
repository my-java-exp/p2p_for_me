from config.p2p_funcs import download, upload, returnFileslist

server_commands = {
    "DOWNLOAD": lambda conn, filename, file_type: upload(conn, filename, file_type),
    "UPLOAD": lambda conn, filename, file_type: download(conn, filename, file_type),
    "uLS": lambda *args: returnFileslist()
}

client_commands = {
    "DOWNLOAD": lambda conn, filename, file_type: download(conn, filename, file_type),
    "UPLOAD": lambda conn, filename, file_type: upload(conn, filename, file_type),
    "mLS": lambda *args: returnFileslist()
}

