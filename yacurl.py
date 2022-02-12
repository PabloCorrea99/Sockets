import socket 
from bs4 import BeautifulSoup


def client(url):
    if("https://" in url):
        url_temp = url.split("https://")[-1]
    elif("http://" in url):
        url_temp = url.split("http://")[-1]
    else:
        url_temp = url
    
    url_temp = url_temp.split("/")[0]
    print(url_temp)
    # AF_INET especifica el protocolo IPv4. En caso de querer hacer uso de IPv6 usar: AF_INET6
    # SOCK_STREAM especifica el uso del protocolo TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    client.connect((url_temp, 80)) 
    str_request = f'GET / HTTP/1.1\r\nHost:{url_temp}\r\nConnection: close\r\n\r\n'
    client.send(bytes(str_request,'utf-8'))
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
    with open(f'{url_temp}.html', 'wb') as f: 
        f.write(html)

    searchStatic(str(html), url_temp)

def searchStatic(html,url):
    parsed_html = BeautifulSoup(html, 'html.parser')
    static_array = []
    for link in parsed_html.find_all('link'):
        try:
            if("image" in link.get("type") or "text" in link.get("type")):
                static_array.append(link)
        except:
            pass
    for img in parsed_html.find_all('img'):
        static_array.append(img)
    
    for new_static in static_array:
        downloadStatic(new_static, url)

def downloadStatic(new_static, url):
    url_temp = ""
    archive_type = "wb"
    if(new_static.name == "img"):
        url_temp = new_static.get("src")
        archive_type = "rb"
    else:
        url_temp = new_static.get("href")
    name = str(url_temp).split("/")[-1]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print(url_temp)
    client.connect((url, 80)) 
    str_request = f'GET {url_temp} HTTP/1.1\r\nHost:{url}\r\nConnection: close\r\n\r\n'
    client.send(bytes(str_request,'utf-8'))

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


    header, archive = data.split(b'\r\n\r\n', 1) 
    print(header.decode('utf-8')) 
    with open(f'{name}', archive_type) as f: 
        f.write(archive)

def main():
    askContinue = True
    while askContinue:
        answer = input("Escriba la url que desee consultar: ")
        client(answer)
        answer_2 = input("Desea continuar?: (SI/NO) ")
        if(answer_2.lower()=="no"):
            askContinue = False
        
main()

        