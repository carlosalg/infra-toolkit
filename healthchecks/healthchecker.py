import json


def healthcheker(data):

    print(data)


def main():
    with open("network_scan_report.json", "r") as f:
        data = json.load(f)

    running_services = [
        {
            "ip": host["ip"],
            "puerto": service["port"],
            "servicio": service["name"]
        }
        for host in data["hosts"]
        for service in host["services"]
    ]

    healthcheker(running_services)


main()
