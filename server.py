import os
import socket
import json


class Program:
    def __init__(self):
        self.directory = os.getcwd()

    def update_directory(self, _directory):
        self.directory = os.path.dirname(_directory)

    def get_directory_data(self):
        file_info = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                stat_info = os.stat(file_path)
                file_info.append({
                    "name": file,
                    "path": file_path,
                    "size": stat_info.st_size,
                    "last_modified": stat_info.st_mtime
                })
        return file_info

    @staticmethod
    def save_file_info(file_info):
        with open("files_info.json", "w") as json_file:
            json.dump(file_info, json_file, indent=4)

    @staticmethod
    def get_binary_file_info():
        with open("files_info.json", "rb") as json_file:
            data = json_file.read()
            return data


prog = Program()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 65432))
s.listen(3)


def handle_commands(client):
    data = client.recv(1024)
    if data.decode().startswith('CH_DIR'):
        new_dir = data.decode().split('CH_DIR', 1)[1].strip()
        prog.update_directory(new_dir)
        client.sendall(b'ok your changes accepted')

    if data.decode() == 'GET_FILE':
        prog.save_file_info(prog.get_directory_data())
        file_data = prog.get_binary_file_info()
        client.sendall(file_data)


while True:
    client_socket, address = s.accept()
    print("Connected by", address)
    handle_commands(client_socket)
    client_socket.close()



