
import ruamel.yaml

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")


print('Hello, This python script will wrap through the variables needed to generate var file for ansible playbook.')
print('USB Variables:')
mount_path = str(input('1/2 - Enter mount path: ') or ("/mnt/usb/"))
mount_uuid = str(input('2/2 - Enter UUID of device: ') or (""))

print('DNSMasq Variables:')
dnsmasq_logging = yes_or_no("Enable DNSMasq logging? ")
network_range = str(input("Enter the network range: ") or ("192.168.1.0"))
dhcp_proxy = yes_or_no(
    "Configure DNSMasq as proxy? (almost certainly answer 'yes')")
tftp = yes_or_no("Enable TFTP? ")
if tftp == True:
    tftp_root = str(input("Enter the TFTP root path: ")
                    or ("/mnt/usb/tftpboot"))
else:
    tftp_root = "/mnt/usb/tftpboot"
pxe_service = str(input("Enter PxE service (probably best left as default): ") or (
    "'X86PC,\"PXE Boot...\",pxelinux'"))
dns_enabled = yes_or_no("Enable DNS? ")
port = int(input('Enter DNS port:') or 53)
dns_upstream = str(
    input("Enter upstream DNS IP (normally your home router): ") or ("192.168.1.1"))
dns_domainname = str(
    input("Enter domain name for homelab: ") or ("homelab.local"))
dns_statichosts = str(input("Enter path for DNS static hosts file: ") or (
    "/etc/dnsmasq_static_hosts.conf"))

print('nginx Variables:')
nginx_service_name = str(
    input("Enter service name for nginx service: ") or ("nginx"))
nginx_port = str(
    input("Enter port for nginx: ") or ("80"))
nginx_root = str(
    input("Enter path for nginx files: ") or ("/mnt/usb/www/html"))

print('ESXi Host Variables:')
hostname = str(
    input("Enter ESXi hostname: ") or ("esx1"))
hostname_fqdn = hostname + "." + dns_domainname
root_passwd = str(
    input("Enter root password for ESXi: ") or ("VMware1!"))
macaddress = str(
    input("Enter MAC address of physical host (e.g. 34:17:eb:ba:2c:c1): ") or (
        "34:17:eb:ba:2c:c1")
)
ip_addr = str(
    input("ENter IP address for physical host: ") or ("192.168.1.11")
)
ip_subnetmask = str(
    input("Enter subnetmask for physical host: ") or ("255.255.255.0"))
ip_gateway = str(
    input("Enter default gateway for physical host: ") or ("192.168.1.1"))
ip_nameserver = str(
    input("Enter DNS server for physical host: ") or ("192.168.1.44")
)
major_version = str(
    input("Enter major ESXi version (e.g. for 6.7 - 67 or 6.5 - 65): ") or ("67")
)
minor_version = str(
    input("Enter minor ESXi version (e.g. u3 for Update 3): ") or ("u3")
)
refresh = yes_or_no("Refresh all files? ")

print('NFS Variables:')
nfs_root = str(
    input("Enter NFS path: ") or ("/mnt/usb/nfs")
)
pfsense_ip_addr = str(
    input("Enter IP address of pfsense VM: ") or ("192.168.1.12")
)

print('Network Variables:')
homelab_subnet = str(
    input("Enter the subnet of the homalb network (e.g. 16 for a 255.255.0.0): ") or ("16")
)
homelab_network = str(
    input("Enter network address for homelab network (e.g. 10.64.0.0): ") or ("10.64.0.0")
)

print('DNS Entries:')
pimaster_ip = str(
    input("Enter IP of PiMaster: ") or ("192.168.1.44")
)
pimaster_dns = pimaster_ip + " " + "pimaster." + dns_domainname
esx_dns = ip_addr + " " + hostname_fqdn
pfsense_dns = pfsense_ip_addr + " " + "pfsense." + dns_domainname
vcsa_ip = str(
    input("Enter IP of VCSA: ") or ("10.64.0.20")
)
vcsa_dns = vcsa_ip + " " + "vcsa." + dns_domainname
dnslist = [pimaster_dns, esx_dns, pfsense_dns, vcsa_dns]
yamldict = {
    "usb_vars": {
        "mount_path": mount_path
    },
    "dnsmasq_vars": {
        "log": dnsmasq_logging,
        "network_range": network_range,
        "dhcp_proxy": dhcp_proxy,
        "tftp": tftp,
        "tftp_root": tftp_root,
        "pxe_service": pxe_service,
        "dns_enabled": dns_enabled,
        "port": port,
        "dns_upstream": dns_upstream,
        "dns_domainname": dns_domainname,
        "dns_statichosts": dns_statichosts
    },
    "nginx_vars": {
        "nginx_service_name": nginx_service_name,
        "nginx_port": nginx_port,
        "nginx_root": nginx_root
    },
    "esxi_host": {
        "hostname": hostname_fqdn,
        "root_passwd": root_passwd,
        "macaddress": macaddress,
        "ip_addr": ip_addr,
        "ip_subnetmask": ip_subnetmask,
        "ip_gateway": ip_gateway,
        "ip_nameserver": ip_nameserver,
        "major_version": major_version,
        "minor_version": minor_version,
        "tftp_root": tftp_root,
        "refresh": refresh,
        "nginx_root": nginx_root
    },
    "nfs_vars": {
        "nfs_root": nfs_root,
        "esx_ip_addr": ip_addr,
        "pfsense_ip_addr": pfsense_ip_addr
    },
    "network_vars": {
        "pfsense_ip": pfsense_ip_addr,
        "homelab_subnet": homelab_subnet,
        "homelab_network": homelab_network 
    },
    "dns_entries":  dnslist
}
print(yamldict)

with open('main.yml', 'w') as outfile:
    yaml.dump(yamldict, outfile, default_flow_style=False, explicit_start=True)
