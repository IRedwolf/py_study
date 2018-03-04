import sys
import socket
import threading


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listenting sockets or correct permissions.")
        sys.exit(0)
    print("[*] Listenting on %s:%d" %(local_host, local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # 打印出本地连接信息

        print("[==>] Received incoming connection from %s:%d" %(addr[0], addr[1]))

        # 开启一个线程和远程主机通信
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port,
                                                                     receive_first))
        proxy_thread.start()


def proxy_handler(client_socket ,remote_host, remote_port,receive_first):

    # 连接远程主机
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # 如果必要从远程主机接收数据
    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # 发送给我们的响应处理
        remote_buffer = response_handler(remote_buffer)

        # 如果我们有数据传递给本地客户端，发送它
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." %len(remote_buffer))
            client_socket.send(remote_buffer)
    # 现在我们从本地循环读取数据，发送给远程主机和本地主机
    while True:

        # 从本地读取数据
        local_buffer = receive_from(client_socket)

        if len(local_buffer):

            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            # 发送给我们的本地请求
            local_buffer = request_handler(local_buffer)
            print("[==>] Sent to remote.")

        # 接受响应数据
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):

            print("[<==] Reveived %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # 发送道响应处理函数
            remote_socket.send(remote_buffer)

            print("[<==] Send to localhost.")

        # 如果两边都没有数据，关闭连接

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")

            break


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2
    print(str)
    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join(["%0*X" % (digits, (x)) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append("%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text))
    print('\n'.join(result))


def receive_from(connection):
    buffer = b""

    # 我们设置了两秒的超时，这取决于目标的情况，可能需要调整

    connection.settimeout(2)

    try:
        # 持续从缓存中读取数据直到没有数据或者超时
        while True:
            data = connection.recvfrom(4096)
            if not data:
                break

            buffer += data

    except:

        pass

    return buffer


def request_handler(buffer):
    # 执行包的修改
    return buffer


def response_handler(buffer):
    return buffer


def main():
    # 命令解析
    if len(sys.argv[1:]) != 5:
        print("Usage:./tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example:./tcp_proxy 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # 设置本地监听参数
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # 设置远程目标
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # 告诉代理在发送给远程主机之前的连接和接受数据
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # 现在设置好我们的监听socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)



