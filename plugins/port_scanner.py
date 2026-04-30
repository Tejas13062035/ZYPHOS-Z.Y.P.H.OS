import socket
import concurrent.futures

TOOL_NAME = "port_scanner"
TOOL_DESCRIPTION = "Scan open ports on a target IP address"
TOOL_ARGS = {"target": "IP address to scan", "ports": "port range e.g. 1-1000"}

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5000: "Flask/Dev", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def scan_port(target: str, port: int) -> dict:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            service = COMMON_PORTS.get(port, "unknown")
            return {"port": port, "status": "open", "service": service}
    except:
        pass
    return None

def run(args: dict) -> dict:
    target = args.get("target", "")
    ports_arg = args.get("ports", "1-1000")

    if not target:
        return {"error": "target IP required"}

    # parse port range
    if "-" in ports_arg:
        start, end = ports_arg.split("-")
        ports = range(int(start), int(end) + 1)
    else:
        ports = [int(p) for p in ports_arg.split(",")]

    print(f"PORT SCAN: {target} ({len(list(ports))} ports)...")

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(target, p), ports)
        for r in results:
            if r:
                open_ports.append(r)
                print(f"  OPEN: {r['port']} ({r['service']})")

    return {
        "status": "ok",
        "target": target,
        "open_ports": len(open_ports),
        "ports": open_ports
    }
