import socket
import time
import logging

logger = logging.getLogger("healthcheck.tcp_check")
def tcp_check(host, port, timeout=5):
    logger.info(f"Starting tcp check on {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result =sock.connect_ex((host,port))
        sock.close()
        return result == 0
    except socket.error as e:
        logger.error(f"TCP check failed: {e}")
        return false

def banner_grabbing(host,port, timeout=5):
    logger.info(f"Starting banner grabbing check on {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        banner = sock.recv(1024).decode('utf-8',errors= 'ignore').strip()
        sock.close()
        return banner
    except Exception:
        logger.warning("Banner not found")
        return None

def latency_check(host, port, timeout=5):
    logger.info(f"Starting TCP latency check on {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        start = time.perf_counter()
        sock.connect((host,port))
        latency = (time.perf_counter () - start) * 1000
        sock.close()
        return round(latency,2)
    except Exception:
        logger.warning("Latency check time out")
        return None

def run_tcp_checks(host,port):
    return {
        "tcp_open": tcp_check(host,port),
        "banner": banner_grabbing(host,port),
        "latency_ms": latency_check(host,port)
    }