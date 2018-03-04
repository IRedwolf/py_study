import socket
target_host = "www.baidu.com"
target_port = 80
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET表示IPv4, socket.SOCK_STREAM 表示TCP协议
client.connect((target_host, target_port))
# 参数是一个tuple，包含地址和端口号。
data = "GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n"
client.send(data.encode('utf8'))
response = client.recv(4096)
print(response.decode('utf8'))
client.close()
