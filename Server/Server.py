import os
import threading
import sys
sys.path.append(os.path.join(os.getcwd(), ".."))
from Utility.utilities import *

# Transmission data spacer
Separator = '<SEPARATOR>'
# Threads status flags
flag_finished_server = True
# Files directory
Directory = 'Files'


def receive_choice(address):
    choice = receive_data(address)
    print(f'{choice}')
    return choice


def reply_list():
    global flag_finished_server
    flag_finished_server = False

    data = '\r\n' + str(os.listdir(Directory)) + '\r\n'
    send_info(client_address, data)
    print('inviato')

    flag_finished_server = True


def reply_get():
    global flag_finished_server
    flag_finished_server = False

    file_name = receive_choice(client_address)
    print(file_name)
    if os.path.exists(os.path.join(Directory, file_name)):
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
