import requests
import logging

logger = logging.getLogger("healthcheck.https_check")

def http_check(host, port, timeout=5):
    for scheme in ("https", "http"):
        logger.info(f"Starting HTTPS check on {host}:{port}")
        try:
            url = f"{scheme}://{host}:{port}"
            response = requests.get(url, timeout=timeout, verify=False)
            return {
                "url": url,
                "status_code": response.status_code,
                "server": response.headers.get("Server", "unknown")
            }
        except requests.RequestException:
            logger.warning(f"Server timeout on {host}:{port}")
            continue
    return None
