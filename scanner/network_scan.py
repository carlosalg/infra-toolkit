import subprocess

def scanner(target):
    network_hosts = f"sudo nmap -T4 -sn -PS22,80,443,3389 -PA80 -PU53 -PP -oX - {target}"
    result = subprocess.run(network_hosts, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print("---Done looking for hosts---\n")
    print("---Looking for hosts with open ports---\n")
    open_ports = "nmap -T4 --open -iL hosts_active.txt"
    op_results = subprocess.run(open_ports,shell=True, capture_output=True, text=True)
    print(op_results.stdout)

    print("---Done looking for hosts with open ports---\n")
    print("---Looking for active services---\n")
    active_services = "nmap -T4 --open -sV -iL hosts_active.txt"
    as_results = subprocess.run(active_services, shell=True, capture_output=True, text=True)
    print(as_results.stdout)
    

def main():
    target_cidr = input("Please enter the target CIDR:")
    scanner(target_cidr)

main()
