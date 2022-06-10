import socket as sk
import threading
import tqdm
import os
from time import sleep

# Transmission data spacer
Separator = '<SEPARATOR>'
# Threads status flags
flag_finished_server = True


def receive_choice(address):
    udp_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    udp_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    udp_socket.bind(address)
    choice = udp_socket.recvfrom(4096)
    choice = choice[0].decode('utf-8')
    print(f'{choice}')

    udp_socket.close()
    return choice


def receive_file(address):
    # File buffer
    buffer_size = 4096 * 10

    udp_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    udp_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    udp_socket.bind(address)
    recv_data = udp_socket.recvfrom(buffer_size)
    recv_file_info = recv_data[0].decode('utf-8')  # Storing the received data, Filename
    # print(f'Received file information {recv_file_info}')
    c_address = recv_data[1]  # Storing the address information of the costumer
    # Print client ip
    print(f'Client {c_address} Connect')
    chosen_file_name, file_size = recv_file_info.split(Separator)
    # Get the name of the file, Size
    chosen_file_name = os.path.basename(chosen_file_name)
    # print(chosen_file_name)

    file_size = int(file_size)

    # File receiving processing
    progress = tqdm.tqdm(range(file_size), f'Receive {chosen_file_name}', unit='B', unit_divisor=1024, unit_scale=True)

    with open('r_' + chosen_file_name, 'wb') as f:
        for _ in progress:
            # Read data from client

            bytes_read = udp_socket.recv(buffer_size)
            # If there is no data transfer content
            if bytes_read == b'file_upload_exit':
                print('Complete transmission!')
                break
            # Read and write
            f.write(bytes_read)
            # Update progress bar
            progress.update(len(bytes_read))

    udp_socket.close()


def send_file(address, filename):
    # Server information
    host, port = address

    # File buffer
    buffer_size = 4096*10
    # Transfer file name
    filename = filename
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
                s.sendall('file_download_exit'.encode('utf-8'))
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)

    # Close resources
    s.close()


def send_info(address, chosen_data):
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    host, port = address

    s.connect((host, port))
    s.send(chosen_data.encode())

    s.close()


def reply_list():
    global flag_finished_server
    flag_finished_server = False

    data = '\r\n' + str(os.listdir()) + '\r\n'
    send_info(client_address, data)
    print('inviato')

    flag_finished_server = True


def reply_get():
    global flag_finished_server
    flag_finished_server = False

    file_name = receive_choice(client_address)
    print(file_name)
    if os.path.exists(file_name):
        send_info(client_address, '1')
        send_file(client_address, file_name)
    else:
        send_info(client_address, '0')

    flag_finished_server = True


def reply_put():
    global flag_finished_server
    flag_finished_server = False

    receive_file(client_address)

    flag_finished_server = True


def thread_cycle(thread):
    thread.start()
    while not flag_finished_server:
        {}
    thread.join()


if __name__ == '__main__':
    client_address = ('localhost', 10000)
    num_clients = 0

    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    while True:
        match receive_choice(client_address):
            case 'list':
                list_thread = threading.Thread(target=reply_list)
                thread_cycle(list_thread)

            case 'get':
                get_thread = threading.Thread(target=reply_get)
                thread_cycle(get_thread)

            case 'put':
                put_thread = threading.Thread(target=reply_put())
                thread_cycle(put_thread)

            case 'exit':
                break

    sock.close()
