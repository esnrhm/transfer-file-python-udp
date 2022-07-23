
import socket
import tqdm
import os
import threading


def write_to_file(list_,file_name):
    f=open('res_'+file_name,'wb')
    for i in list_:
        f.write(i)
    f.close()


def recvived(address, port):

    SEPARATOR = '/'
    Buffersize = 4096*10

    while True:
        print(' Prepare to receive new files ...')

        udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.bind((address, port))
        recv_data = udp_socket.recvfrom(Buffersize)
        recv_file_info = recv_data[0].decode('utf-8')  
        print(f' Received file information {recv_file_info.split(SEPARATOR)}')
        c_address = recv_data[1] 
        
        print(f' Client {c_address} Connect ')
        
        filename ,file_size = recv_file_info.split(SEPARATOR) 
        filename = os.path.basename(filename)
        file_size = int(file_size)

        progress = tqdm.tqdm(range(file_size), f' Receive {filename}', unit='B', unit_divisor=1024, unit_scale=True)
        _list=[]
        for _ in progress:
            bytes_read = udp_socket.recv(Buffersize)
            if bytes_read == b'file_download_exit':
                print(' Complete transmission! ')
                break
            _list.append(bytes_read) 
            progress.update(len(bytes_read))
        udp_socket.close()
        t1 = threading.Thread(target=write_to_file, args=(_list, filename))
        t1.start()
        del _list

if __name__ == '__main__':

    port = 1235
    address = "127.0.0.1"
    t = threading.Thread(target=recvived, args=(address, port))
    t.start()

