import socket
from program import Program


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



