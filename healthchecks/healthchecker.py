import json
import logging
import sys
from datetime import datetime
from .checks.tcp_check import run_tcp_checks as tcp
from .checks import https_rcheck as httpsrc
from .checks.dns_check import run_dns_check as dns
from .checks.ssl_check import run_ssl_checks as ssl 


#Logger config

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('healthcheck_scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("healtcheck")

HEALTH_CHECKS = {
    "tcp" : tcp,
    "http_s": httpsrc.http_check,
    "dns": dns,
    "ssl": ssl
}

def healthcheker(data, dns_test_hostname="google.com"):
    results = []
    for entry in data:
        ip = entry["ip"]
        port = entry["port"]
        logger.info(f"Checking {ip}:{port} ({entry['service']})")
        result = {
        "ip": ip,
        "port": port,
        "service": entry["service"],
        "tcp": HEALTH_CHECKS["tcp"](ip,port),
        "http_s": HEALTH_CHECKS["http_s"](ip,port),
        "dns": HEALTH_CHECKS["dns"](dns_test_hostname,ip) if port == 53 else None,
        "ssl": HEALTH_CHECKS["ssl"](ip, port) if port == 443 else None,
        }
        logger.debug(f"Result for {ip}:{port} - {result}")
        results.append(result)

    report_data = {
        "healtcheck_report":{
            "report_generated":  datetime.now().isoformat(), 
            "scanner_source": "network_scan_report.json",
            "total_hosts_checked": len(set(entry["ip"]for entry in data)),
            "services_checked": len(set(entry["service"] for entry in data))
        },
        "hosts": results,
        "summary": {
            "total_hosts": len(set(r["ip"] for r in results)),
            "total_services": len(results),
            "services_down": sum(1 for r in results if not r["tcp"]["tcp_open"]),
            "http_200": sum(1 for r in results if r["http_s"] and r["http_s"]["status_code"] == 200),
            "ssl_expiring_soon": sum(1 for r in results if r["ssl"] and r["ssl"].get("expiring_soon")),
            "ssl_expired": sum(1 for r in results if r["ssl"] and r["ssl"].get("is_expired")),
            "dns_servers_found": sum(1 for r in results if r["dns"] is not None),
        }

    }

    with open('./network_healthcheck_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)

    logger.info("Finished Network Health Checks")

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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\n HealthChecks interrupted by user (Ctrl+C)")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unhandled fatal error: {e}")
        logger.exception("Stacktrace complete:")
        sys.exit(1)
