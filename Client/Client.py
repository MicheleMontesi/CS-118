import threading
from time import sleep
import socket as sk
import tqdm
import os

welcome_message = '\r\nClient-Server Project\r\n\r\n' \
                  'Available options:\r\n\r\n' \
                  '> list)\tReturn the list of the downloadable files on the server\r\n' \
                  '> get)\tDownload a file from the server, given a name\r\n' \
                  '> put)\tUpload a file on the server\r\n' \
                  '> exit)\tExit the client and shuts down the server\r\n'

# Transmission data spacer
Separator = '<SEPARATOR>'
# Threads status flags
flag_finished = True


def send_choice(address, taken_choice):
    host, port = address
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    s.connect((host, port))
    s.send(f'{taken_choice}'.encode('utf-8'))
    s.close()


def send_file(address, chosen_file_name):
    # Server information
    host, port = address

    # File buffer
    buffer_size = 4096 * 10
    # Transfer file name
    filename = chosen_file_name
    # File size
    file_size = os.path.getsize(filename)
    # Create socket link

    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    print(f'Server connection {host}:{port}')
    s.connect((host, port))
    print('Successful connection to server')

    # Send file name and size, which must be encoded
    sleep(1)
    s.send(f'{filename}{Separator}{file_size}'.encode('utf-8'))

    # File transfer
    progress = tqdm.tqdm(range(file_size), f'Send {filename}', unit='B', unit_divisor=1024)

    with open(filename, 'rb') as f:
        # Read the file
        for _ in progress:
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                print('Exit transmission, transmission is complete!')
                s.sendall('file_upload_exit'.encode('utf-8'))
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)

    # Close resources
    s.close()


def receive_file(address):
    # File buffer
    buffer_size = 4096 * 10

    udp_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    udp_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    udp_socket.bind(address)
    recv_data = udp_socket.recvfrom(buffer_size)
    recv_file_info = recv_data[0].decode('utf-8')   # Storing the received data, Filename
    c_address = recv_data[1]    # Storing the address information of the costumer
    print(f'Client {c_address} Connect')
    chosen_file_name, file_size = recv_file_info.split(Separator)
    # Get the name of the file, Size
    chosen_file_name = os.path.basename(chosen_file_name)

    file_size = int(file_size)

    # File receiving processing
    progress = tqdm.tqdm(range(file_size), f'Receive {chosen_file_name}', unit='B', unit_divisor=1024, unit_scale=True)

    with open('r_' + chosen_file_name, 'wb') as f:
        for _ in progress:
            # Read data from client

            bytes_read = udp_socket.recv(buffer_size)
            # If there is no data transfer content
            if bytes_read == b'file_download_exit':
                print('Complete transmission!')
                break
            # Read and write
            f.write(bytes_read)
            # Update progress bar
            progress.update(len(bytes_read))

    udp_socket.close()


def receive_data(address):
    udp_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    udp_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    udp_socket.bind(address)
    recv_data = udp_socket.recvfrom(4096)
    recv_data = recv_data[0].decode('utf-8')
    udp_socket.close()
    return recv_data


def receive_info(address):
    print(f'List of files:\r\n{receive_data(address)}\r\n')


def ask_list():
    global flag_finished
    flag_finished = False

    os.system('cls' if os.name == 'nt' else 'clear')
    print(welcome_message)
    send_choice(server_address, choice)
    receive_info(server_address)

    flag_finished = True


def ask_get():
    global flag_finished
    flag_finished = False

    os.system('cls' if os.name == 'nt' else 'clear')
    send_choice(server_address, choice)
    file_name = input('Insert the name of the file to download from the server\r\n> ')
    send_choice(server_address, file_name)
    if receive_data(server_address) == '1':
        receive_file(server_address)
        print(welcome_message)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\r\nThis file doesn\'t exists in the server, chose an existing file.\r\n')
        print(welcome_message)

    flag_finished = True


def ask_put():
    global flag_finished
    flag_finished = False

    os.system('cls' if os.name == 'nt' else 'clear')
    file_name = input('Insert the name of the file to upload to the server\r\n> ')
    print(file_name)
    if os.path.exists(file_name):
        send_choice(server_address, choice)
        send_file(server_address, file_name)
        print(welcome_message)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\r\nThis file doesn\'t exists in local, chose an existing file.\r\n')
        print(welcome_message)

    flag_finished = True


def thread_cycle(thread):
    thread.start()
    while not flag_finished:
        {}
    thread.join()


if __name__ == '__main__':
    server_address = ('localhost', 10000)

    print(welcome_message)
    while True:
        choice = input('> ')
        match choice:
            case 'list':
                list_thread = threading.Thread(target=ask_list)
                thread_cycle(list_thread)

            case 'get':
                get_thread = threading.Thread(target=ask_get)
                thread_cycle(get_thread)

            case 'put':
                put_thread = threading.Thread(target=ask_put)
                thread_cycle(put_thread)

            case 'exit':
                send_choice(server_address, choice)
                break

            case _:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('You have to insert one of the four options:\r\n')
                print(welcome_message)
