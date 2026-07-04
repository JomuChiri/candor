# candor/core/validate.py
import re
import ipaddress

def is_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False
        
def validate_target(target: str) -> bool:
    # Hostname/domain
    hostname_pattern = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$")
    if hostname_pattern.match(target):
        return True
    return False
