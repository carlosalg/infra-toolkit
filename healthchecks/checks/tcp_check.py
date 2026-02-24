import socket


def tcp_check(host, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result =sock.connect_ex((host,port))
        sock.close()
        return result == 0
    except socket.error as e:
        return false
