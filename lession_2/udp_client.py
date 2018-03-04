import socket

target_host = "127.0.0.1"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


data = "123".encode("UTF8")

client.sendto(data, (target_host, target_port))

data, addr = client.recvfrom(4096)

print(data.decode("UTF8"))

