import socket
import requests

def get_my_ip():
    """Get the current public IP address"""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception as e:
        print(f"Error getting IP: {e}")
        return None

def check_ip(access_key, ip_address=None):
    """
    Check if an IP is blacklisted using Project Honey Pot's HTTP:BL
    
    Args:
        access_key (str): Your Project Honey Pot access key
        ip_address (str, optional): IP address to check. If None, gets current IP
    """
    if ip_address is None:
        ip_address = get_my_ip()
        if ip_address is None:
            return
        
    print(f"Checking IP: {ip_address}")
    
    # Reverse the IP address octets
    reversed_ip = '.'.join(ip_address.split('.')[::-1])
    
    # Create the lookup domain
    lookup = f"{access_key}.{reversed_ip}.dnsbl.httpbl.org"
    
    try:
        # Perform the DNS lookup
        result = socket.gethostbyname(lookup)
        
        # Parse the response
        octets = result.split('.')
        if len(octets) == 4:
            days_since_last_activity = int(octets[1])
            threat_score = int(octets[2])
            visitor_type = int(octets[3])
            
            print("\nResults from Project Honey Pot:")
            print(f"Days since last suspicious activity: {days_since_last_activity}")
            print(f"Threat score: {threat_score}")
            print(f"Visitor type: {visitor_type}")
            
            if visitor_type == 0:
                print("\n✅ IP appears to be clean!")
            else:
                print("\n⚠️  IP may be suspicious.")
                print("\nVisitor types:")
                print("0: Search Engine, 1: Suspicious, 2: Harvester")
                print("4: Comment Spammer, 8: Bad Robot")
                
            return visitor_type == 0
                
    except socket.gaierror:
        print("\n✅ IP not found in Project Honey Pot's database (this is good!)")
        return True
    except Exception as e:
        print(f"\n❌ Error checking IP: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Check IP status with Project Honey Pot')
    parser.add_argument('access_key', help='Your Project Honey Pot access key')
    parser.add_argument('--ip', help='IP address to check (optional)', default=None)
    
    args = parser.parse_args()
    check_ip(args.access_key, args.ip) 