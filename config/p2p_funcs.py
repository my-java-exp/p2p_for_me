from pydoc import text
import socket
import os
import datetime
import time

from config.p2p_constants import BUFFER_SIZE, UPLOAD_PATH, DOWNLOAD_PATH, LOG_FILE

def returnFileType(filename):
    text_files = [".txt", ".csv", ".json", ".xml", ".html", ".md", ".log", ".yaml", ".yml", ".ini", ".cfg", ".conf", ".py", ".java", ".cpp", ".js", ".css", ".sh", ".bat", ".ps1", ".rb", ".php", ".go", ".rs", ".swift", ".kt", ".dart", ".lua", ".sql", ".pl", ".pm", ".r", ".m", ".sas", ".spss", ".stata", ".sas7bdat", ".sav", ".dta", ".por", ".xlsx", ".xls", ".docx", ".doc", ".pptx", ".ppt"]
    if any(filename.endswith(ext) for ext in text_files):
        return "text file"
    else:
        return "bytes file"

def download(conn: socket.socket, filename, file_type="bytes file"):

    full_filename= f"{DOWNLOAD_PATH}/{filename}"

    if file_type != "bytes file": # Check the file type
        with open(full_filename, "w") as f:
            while True:
                data: bytes = conn.recv(BUFFER_SIZE) # Dont decode yet

                if not data: # Check if data is still being sent else break from loop
                    break

                f.write(data.decode()) # Write decoded data into file
        
    else:
        # Do the same thing but dont decode data
        with open(full_filename, "wb") as f:
            while True:
                data: bytes = conn.recv(BUFFER_SIZE)

                if not data:
                    break

                f.write(data)

def upload(conn: socket.socket, filename, file_type="bytes file"):
    
    full_filename = f"{UPLOAD_PATH}/{filename}"
    if not os.path.exists(full_filename):
        # Log that file does not exist and send error message to client
        return ""

    with open(full_filename, "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)

            if not data:
                break

            conn.sendall(data)
    
    return ""

def log(message):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                f.write(f"[{timestamp}] Created log file\n")
            
        with open(LOG_FILE, "+a") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    except Exception as e:
        print(f"Error logging message: {e}")
        return

def lambda_log(conn: socket.socket, message: str, message_to_user: str):
    log(message)
    conn.sendall(message_to_user.encode())