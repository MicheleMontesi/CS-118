import os
import threading
import sys
sys.path.append(os.path.join(os.getcwd(), ".."))
from Utility.utilities import *

welcome_message = '\r\nClient-Server Project\r\n\r\n' \
                  'Available options:\r\n\r\n' \
                  '> list)\tReturn the list of the downloadable files on the server\r\n' \
                  '> get)\tDownloadedFiles a file from the server, given a name\r\n' \
                  '> put)\tUpload a file on the server\r\n' \
                  '> exit)\tExit the client and shuts down the server\r\n'

# Threads status flags
flag_finished = True
# Files directory
Directory = 'Files'


def send_choice(address, taken_choice):
    send_info(address, f'{taken_choice}')


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
    if os.path.exists(os.path.join(Directory, file_name)):
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
