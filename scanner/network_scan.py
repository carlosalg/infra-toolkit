import subprocess
import xml.etree.ElementTree as et
import logging
from datetime import datetime
import json
import sys

#Logger config
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers =[
        logging.FileHandler('network_scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def nmap_runner(cmd: List[str]) -> Optional[str]:
    logger.info(f"Starting nmap with command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        logger.info("Nmap command was completed successfully!")
        logger.debug(f"Stdout: {result.stdout[:200]}...")

        if result.stderr:
            logger.warning(f"Stderr: {result.stderr}")

        return result.stdout
        
    except FileNotFoundError:
        logger.error("Error: nmap is not installed or in the system PATH")
        return None

    except subprocess.CalledProcessError as e:
        logger.error(f"Error: nmap finished with exit code {e.returncode}")
        logger.error(f"Command: {' '.join(cmd)}")
        logger.error(f"Stdout: {e.stdout}")
        logger.error(f"Stderr: {e.stderr}")

        if "You requested a scan type which requires root privileges" in e.stderr:
            logger.error("SOLUTION: run script with sudo priviligies")
        elif "Failed to resolve" in e.stderr:
            logger.error("SOLUTION: Check if target/hostname is correct")
        elif "network is unreachable" in e.stderr:
            logger.error("SOLUTION: Check for network connectivity")
        
        return None

    except PermissionError:
        logger.error("Error: Insufficient permits")
        logger.error("SOLUTION: Run with sudo or as root")
        return None

    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        logger.exception("Stacktrace completed:")
        return None

def scanner(target):

    scan_report = {}

    logger.info(f"=== Starting host discovery on {target} ===")
    
    network_hosts = ['sudo','nmap', '-T4', '-sn', '-PS22,80,443,3389', '-PA80', '-PU53', '-PP', '-oX', '-', target]
    hosts_result = nmap_runner(network_hosts)
    data_results1 = et.fromstring(hosts_result)

    for host in data_results1.findall('.//host'):
        ip = host.find('address').get('addr')
        scan_report[ip]= {
            "ip": ip,
            "status": host.find('status').get('state'),
            "ports":[],
            "services":[]
        }

    # Method to get ip's for other scans
    active_hosts = [
        address.get('addr')
        for host in data_results1.findall('.//host')
        if host.find('status').get('state') == 'up'
        for address in host.findall('address')
        if address.get('addrtype')== 'ipv4'
    ]
    
    logger.info(f"Host discovery completed: {len(active_hosts)} hosts found")

    if not active_hosts:
        logger.warning("No se encontraron hosts activos")
    else:
        logger.debug(f"Hosts founded: {', '.join(active_hosts[:10])}...")


    logger.info(f"=== Starting port scan on {len(active_hosts)} hosts ===")
    
    open_ports = ['nmap', '--open'] + active_hosts + ['-oX','-']
    op_results = nmap_runner(open_ports)
    data_results2 = et.fromstring(op_results)

    for host in data_results2.findall('.//host'):
        ip = host.find('address').get('addr')
        if ip in scan_report:
            for port in host.findall('.//port'):
                scan_report[ip]["ports"].append({
                    "port": port.get('portid'),
                    "state": port.find('state').get('state')
                })
    logger.info("Port scan completed successfully")

    logger.info("=== Searching for active services ===")
    
    active_services = ['nmap','-sV', '-oX','-']+active_hosts
    as_results = nmap_runner(active_services)
    data_results3 = et.fromstring(as_results)

    for host in data_results3.findall('.//host'):
        ip = host.find('address').get('addr')
        if ip in scan_report:
            for service in host.findall('.//service'):
                scan_report[ip]["services"].append({
                    "name": service.get('name'),
                    "product": service.get('product')                                       
                })

    logger.info("Active servces scan completed")

    final_data = {
        "metadata":{
            "report_generated": datetime.now().isoformat(),
            "scanner": "nmap",
            "version": data_results1.get('version'),
            "target_network": target,
            "scan_stages": [
                {"stage": "host_discovery", "completed": data_results1.get('startstr')},
                {"stage": "port_scan", "completed": data_results2.get('startstr')},
                {"stage": "service_detection", "completed": data_results3.get('startstr')}
            ],
            "total_hosts_scanned": len(scan_report)
        },
        "hosts": list(scan_report.values())
    }

    with open('./network_scan_report.json', 'w') as f:
        json.dump(final_data, f, indent=2)

    logger.info("Network Scan Completed")
    

def main():
    target_cidr = input("Please enter the target CIDR:")
    scanner(target_cidr)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user (Ctrl+C)")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unhandled fatal error: {e}")
        logger.exception("Stacktrace complete:")
        sys.exit(1)
