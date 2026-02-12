import subprocess
import xml.etree.ElementTree as et
from datetime import datetime
import json

def scanner(target):

    scan_report = {}
    
    network_hosts = ['sudo','nmap', '-T4', '-sn', '-PS22,80,443,3389', '-PA80', '-PU53', '-PP', '-oX', '-']+[target]
    hosts_result = subprocess.run(network_hosts, capture_output=True, text=True)
    data_results1 = et.fromstring(hosts_result.stdout)

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
    
    print("---Done looking for hosts---\n")
    print("---Looking for hosts with open ports---\n")
    
    open_ports = ['nmap', '--open'] + active_hosts + ['-oX','-']
    op_results = subprocess.run(open_ports, capture_output=True, text=True)
    data_results2 = et.fromstring(op_results.stdout)

    for host in data_results2.findall('.//host'):
        ip = host.find('address').get('addr')
        if ip in scan_report:
            for port in host.findall('.//port'):
                scan_report[ip]["ports"].append({
                    "port": port.get('portid'),
                    "state": port.find('state').get('state')
                })
    

    print("---Done looking for hosts with open ports---\n")
    print("---Looking for active services---\n")
    
    active_services = ['nmap','-sV', '-oX','-']+active_hosts
    as_results = subprocess.run(active_services, capture_output=True, text=True)
    data_results3 = et.fromstring(as_results.stdout)

    for host in data_results3.findall('.//host'):
        ip = host.find('address').get('addr')
        if ip in scan_report:
            for service in host.findall('.//service'):
                scan_report[ip]["services"].append({
                    "name": service.get('name'),
                    "product": service.get('product')                                       
                })

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

    print("Scan Complete!")
    

def main():
    target_cidr = input("Please enter the target CIDR:")
    scanner(target_cidr)

main()
