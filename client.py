
import threading
import socket
import tqdm
import os
from time import ctime, sleep

def send(address, filename):

    SEPARATOR = '/'
    host, port = address

    Buffersize =65507
    filename = filename
    file_size = os.path.getsize(filename)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print(f' Server connection {host}:{port}')
    s.connect((host, port))
    print(' Successful connection to server ')
    s.send(f'{filename}{SEPARATOR}{file_size}'.encode('utf-8'))

    progress = tqdm.tqdm(range(file_size), f' Send {filename}', unit='B', unit_divisor=1024, unit_scale=True)


    with open(filename, 'rb') as f:
        for _ in progress:
            bytes_read = f.read(Buffersize)
            if not bytes_read:
                print('exit Exit transmission, transmission is complete! ')
                sleep(1)
                s.sendall('file_download_exit'.encode('utf-8'))
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)
    s.close()


if __name__ == '__main__':
    address = ('127.0.0.1', 1235)
    filename = input(' Please enter a file name: ')
    t = threading.Thread(target=send, args=(address, filename))
    t.start()
