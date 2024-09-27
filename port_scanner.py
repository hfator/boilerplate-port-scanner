import socket
from common_ports import ports_and_services
import ipaddress

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    if target[0].isalpha():
        try:
            ip_address = socket.gethostbyname(target)
            hostname = target
        except:
            return "Error: Invalid hostname"
    else:
        try:
            ipaddress.ip_address(target)
            ip_address = target
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
            except:
                pass
        except:
            return "Error: Invalid IP address"
    
    for port in range(port_range[0], port_range[1] + 1): 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if not s.connect_ex((ip_address, port)):
            open_ports.append(port)
        s.close()

    if verbose:
        service_info = ""
        try:
            service_info+=f'Open ports for {hostname} ({ip_address})'
        except:
            service_info += f'Open ports for {ip_address}'
        service_info+=("\nPORT     SERVICE")

        for port in open_ports:
            service_name = ports_and_services.get(port)
            service_info += f"\n{port:<7}  {service_name}"
        return service_info
    
    return open_ports