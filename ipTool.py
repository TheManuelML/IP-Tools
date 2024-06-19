import sys
import subprocess
import socket
import platform
import locale
from termcolor import colored


# Identify the operation system
V = "1.0"
OS = platform.system()


# Create the class Net (all about the IP)
class Net():
    def __init__(self, ip : str) -> None:
        self.ip = ip
    
    def classes(self) -> str:
        octets = self.ip.split('.')
        if int(octets[0]) == 127:
            classes = 'A Reserved'
        elif int(octets[0]) >= 1 and int(octets[0]) <= 126:
            classes = 'A'
        elif int(octets[0]) >= 128 and int(octets[0]) <= 191:
            classes = 'B'
        elif int(octets[0]) >= 192 and int(octets[0]) <= 223:
            classes = 'C'
        elif int(octets[0]) >= 224 and int(octets[0]) <= 239:
            classes = 'D'
        elif int(octets[0]) >= 240 and int(octets[0]) <= 254:
            classes = 'E'
        else:
            classes = 'Subnetmask'
        return  classes

    def router(self) -> str:
        octets = self.ip.split('.')
        octets[3] = '1'
        router = '.'.join(octets)
        return router

    def broadcast(self) -> str:
        octets = self.ip.split('.')
        octets[3] = '255'
        broadcast = '.'.join(octets)
        return broadcast

    def net(self) -> str:
        octets = self.ip.split('.')
        octets[3] = '0'
        net = '.'.join(octets)
        return net

    def ping_ip(self) -> None:
        # Selecting the command depending on the OS
        if OS == "Linux" or OS == "Darwin":
            command = f"ping -c 1 {self.ip}"
        elif OS == "Windows":
            command = f"ping -n 1 {self.ip}"
        else:
            print(f"[!] At the moment we do not have commands that support the OS: {OS}")
            return None
        # Executing the command and saving the outputs
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Decoding the ouputs
        str_stdout = output.stdout.decode(locale.getpreferredencoding())
        str_stderr = output.stderr.decode(locale.getpreferredencoding())
        # Printing the output depending of there were errors
        if str_stderr == "":
            print(colored("\n[+] Estandar output:", "green") + f"{str_stdout}\n")
        else:   
            print(colored("\n[+] Estandar output:") + f"{str_stdout}\n" + colored("[+] Estandar error:", "red") + f"{str_stderr}\n")
        return None


## Main functions
def banner() -> None:
    print(f'''\r ___ ____    _____           _ 
            \r|_ _|  _ \  |_   _|__   ___ | |
            \r | || |_) |   | |/ _ \ / _ \| |
            \r | ||  __/    | | (_) | (_) | |
            \r|___|_|       |_|\___/ \___/|_|
          \r\tVersion: {V}''')

def menu() -> None:
    print('''\n
    [1] Information of the address
    [2] Ping the IP address
    [3] Reverse DNS lookup

    [0] Exit
    ''')

def option() -> int:
    op = input("[?] Select an option: ")
    try:
        op = int(op)
    except ValueError:
        print("[!] Invalid option from the MENU")
        sys.exit(1)

    if op == 0:
        print("[+] Exiting the program")
        sys.exit(0)

    if op < 0 or op > 4:
        print("[!] Invalid option from the MENU")
        sys.exit(1)
    return op

def executing(op : int, ip : Net) -> None:
    match op:
        case 1:
            information(ip)
        case 2:
            ping(ip)
        case 3:
            reverse_dns(ip)
    return None

def verify_ip(ip : str) -> bool:
    octets = ip.split('.')
    if len(octets) != 4:
        return False
    for octet in octets:
        try:
            octet = int(octet)
        except (ValueError, TypeError):
            print("[!] This is an invalid IPv4 address")
            sys.exit(1)
        if int(octet) < 0 or int(octet) > 255:
            return False
    return True

def request_ip() -> Net:
    ipv4 = input("[?] Write an IPv4: ")
    if verify_ip(ipv4):
        ip_object = Net(ipv4)
    else:
        print("[!] This is an invalid IPv4 address")
        sys.exit(1)
    return ip_object


## Option 1
def information(ip : Net) -> None:
    print(colored("\n[+] Information about the address:", "green"))
    print(f'''\rIP: {ip.ip}
              \rClass: {ip.classes()}\n''')
    if ip.classes() == 'C' or ip.classes() == 'B' or ip.classes == 'A':
        print(f'''\rNetwork Address: {ip.net()}
                \rBroadcast Address: {ip.broadcast()}
                \rRouter Address: {ip.router()}\n''')
    else:
        return None
    return None

## Option 2
def ping(ip : Net) -> None:
    ip.ping_ip()
    return None

## Option 3
def reverse_dns(ip : Net) -> None:
    try:
        hostname, _, _ = socket.gethostbyaddr(ip.ip)
        print(colored("\n[+] Reverse DNS lookup:", "green"))
        print(f'Hostname: {hostname}')
    except socket.herror:
        print("[!] Unable to recognize the domain of the IPv4")
        sys.exit(1)
    return None


## Main function
def main() -> None:
    banner()
    menu()
    OP = option()
    IP = request_ip()
    executing(OP, IP)
    return None


## Main logic
if __name__ == '__main__':
    main()