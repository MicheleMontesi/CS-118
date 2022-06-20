import os
import socket as sk
from time import sleep
import tqdm

# Transmission data spacer
Separator = '<SEPARATOR>'


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
                s.sendall(b'file_download_exit')
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


def send_info(address, chosen_data):
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    host, port = address

    s.connect((host, port))
    s.send(chosen_data.encode('utf-8'))

    s.close()


def receive_data(address):
    udp_socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    udp_socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    udp_socket.bind(address)
    recv_data = udp_socket.recvfrom(4096)
    recv_data = recv_data[0].decode('utf-8')
    udp_socket.close()
    return recv_data
