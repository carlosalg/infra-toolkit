import requests

def http_check(host, port, timeout=3):
    for scheme in ("https", "http"):
        try:
            url = f"{scheme}://{host}:{port}"
            response = requests.get(url, timeout=timeout, verify=False)
            return {
                "url": url,
                "status_code": response.status_code,
                "server": response.headers.get("Server", "unknown")
            }
        except requests.RequestException:
            continue
    return None
