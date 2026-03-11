import ssl
import socket
from datetime import datetime


def ssl_ccheck(host,port=443,timeout=5):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock) as ssock:
                cert = ssock.getpeercert()
                return {
                    "subject": dict(x[0] for x in cert["subject"]),
                    "issuer" : dict(x[0] for x in cert["issuer"]),
                    "version": cert["version"],
                    "not_before": cert["notBefore"],
                    "not_after": cert["notAfter"],
                    "san": cert.get("subjectAltName", [])
                }
    except Exception as e:
        return {"error": str(e)}

def ssl_echeck(host, port=443, timeout=5):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock) as ssock:
                cert = ssock.getpeercert()
                expiry_str = cert["notAfter"]
                expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
                days_remaining = (expiry_date - datetime.utcnow()).days
                return {
                    "expires_on": expiry_str,
                    "days_remaining": days_remaining,
                    "is_expired": days_remaining < 0,
                    "expiring_soon": 0 <= days_remaining <= 30
                }
    except Exception as e:
        return {"error": str(e)}

def run_ssl_checks(host,port=443):
    return {
        "ssl_cert": ssl_cert_check(hostname, port),
        "ssl_expiry": ssl_expiry_check(hostname, port),
    }
