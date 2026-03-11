import json
from .checks.tcp_check import run_tcp_checks as tcp
from .checks import https_rcheck as httpsrc
from .checks.dns_check import run_dns_check as dns
from .checks.ssl_check import run_ssl_checks as ssl 

HEALTH_CHECKS = {
    "tcp" : tcp,
    "http_s": httpsrc.http_check,
    "dns": dns,
    "ssl": ssl
}

def healthcheker(data, dns_test_hostname="google.com"):
    for entry in data:
        ip = entry["ip"]
        port = entry["port"]
        tcp_results= HEALTH_CHECKS["tcp"](ip,port)
        https =     HEALTH_CHECKS["http_s"](ip,port)
        if port == 53:
            dns_results = HEALTH_CHECKS["dns"](dns_test_hostname,ip)
        if port ==  443:
            ssl_results = HEALTH_CHECKS["ssl"](ip, port)

def main():
    with open("network_scan_report.json", "r") as f:
        data = json.load(f)

    running_services = [
        {
            "ip": host["ip"],
            "port": service["port"],
            "service": service["name"]
        }
        for host in data["hosts"]
        for service in host["services"]
    ]

    healthcheker(running_services)


main()
