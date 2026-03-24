import dns.resolver
import time
import logging

logger = logging.getLogger("healthcheck.dns_check")

def dns_checker(host, dns_server=None):
    logger.info(f"Starting dns check on {host}")
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
        logger.error(f"DNS check failed {host} - {e}")
        return {"resolved":False, "error": str(e)}

def dns_latency_check(host):
    logger.info(f"Stating DNS latency Check on {host}")
    try:
        start = time.perf_counter()
        dns.resolver.resolve(hostname,'A')
        return round((time.perf_counter() - start) * 1000, 2)
    except dns.exception.DNSException:
        logger.warning(f"Latency check timed out {host}")
        return None

def run_dns_check(hostname, dns_server):
    return {
        "dns": dns_checkerU(hostname, dns_server),
        "dns_latency_ms": dns_latency_check(hostname)
    }