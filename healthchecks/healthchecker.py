import json
from .checks.tcp_check import tcp_check 


HEALTH_CHECKS = {
    "tcp" : tcp_check,
}

def healthcheker(data):
    accion = "tcp"
    for entry in data:
        ip = entry["ip"]
        port = entry["port"]
        result = HEALTH_CHECKS[accion](ip,port)
        print(result)


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
