import socket 

# AF_INET especifica el protocolo IPv4. En caso de querer hacer uso de IPv6 usar: AF_INET6
# SOCK_STREAM especifica el uso del protocolo TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

client.connect(('www.sina.com.cn', 80)) 
client.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# Recibir datos:
buffer = [] 
while True: 
 # Reciba hasta 1k bytes a la vez: 
    response = client.recv(1024) 
    if response: 
        buffer.append(response) 
    else: 
        break 
data = b"".join(buffer)

client.close()


header, html = data.split(b'\r\n\r\n', 1) 
print(header.decode('utf-8')) 
# Escriba los datos recibidos en un archivo: 
with open('sina.html', 'wb') as f: 
    f.write(html)