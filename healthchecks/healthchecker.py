import json
from .checks import tcp_check as checks
from .checks import https_rcheck as httpsrc
from .checks import dns_check as dnsChecks

HEALTH_CHECKS = {
    "tcp" : checks.tcp_check,
    "banner" : checks.banner_grabbing,
    "latency": checks.latency_check,
    "http_s": httpsrc.http_check,
    "dns": dnsChecks.dns_checker,
}

def healthcheker(data):
    action = "tcp"
    action2 = "banner"
    for entry in data:
        ip = entry["ip"]
        port = entry["port"]
        result =    HEALTH_CHECKS[action](ip,port)
        banner =    HEALTH_CHECKS[action2](ip,port)
        latency =   HEALTH_CHECKS["latency"](ip,port)
        https =     HEALTH_CHECKS["http_s"](ip,port)
        dns =       HEALTH_CHECKS["dns"]("google.com",ip)
        print(result,banner,latency)
        print(https)
        print(dns)


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
