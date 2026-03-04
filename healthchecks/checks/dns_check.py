import dns.resolver
import time

def dns_checker(host, dns_server=None):
    try:
        resolver = dns.resolver.Resolver()
        resolver.lifetime= 2
        resolver.timeout=1
        if dns_server:
            resolver.nameservers = [dns_server]
        answers = resolver.resolve(host, 'A')
        return {
            "resolved": True,
            "ips": [r.address for r in answers]
        }
    except dns.exception.DNSException as e:
        return {"resolved":False, "error": str(e)}

def dns_latency_check(host):
    try:
        start = time.perf_counter()
        dns.resolver.resolve(hostname,'A')
        return round((time.perf_counter() - start) * 1000, 2)
    except dns.exception.DNSException:
        return None
