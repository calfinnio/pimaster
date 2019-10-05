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
mount_uuid = str(input('2/2 - Enter UUID of device: ') or ( ""))

print('DNSMasq Variables:')
dnsmasq_logging = yes_or_no("Enable DNSMasq logging? ")
network_range = str(input("Enter the network range: ") or ("192.168.1.0"))
dhcp_proxy = yes_or_no("Configure DNSMasq as proxy? (almost certainly answer 'yes')")
tftp = yes_or_no("Enable TFTP? ")
tftp_root = if tftp == True
pxe_service = str(input("Enter PxE service (probably best left as default): ") or ("'X86PC,\"PXE Boot...\",pxelinux'))
dns_enabled = yes_or_no("Enable DNSM? ")
port =
dns_upstream =
dns_domainname =
dns_statichosts =
print(mount_path)
print(dnsmasq_logging)
print(network_range)
print(dhcp_proxy)
print(tftp)
print(tftp_root)
print(pxe_service)
print(dns_enabled)
print(port)
print(dns_upstream)
print(dns_domainname)
print(dns_statichosts)
#dnsmasq_log = log: true
#    network_range: 192.168.1.0
#    dhcp_proxy: true
#    tftp: true
#    tftp_root: /mnt/usb/tftpboot
#    pxe_service: 'X86PC,"PXE Boot...",pxelinux'
#    dns_enabled: true
#    port: 53
#    dns_upstream: 192.168.1.1
#    dns_domainname: houseofbears.co.uk
#    dns_statichosts: "/etc/dnsmasq_static_hosts.conf"
#dnsmasq_vars:
#  - log: true
#    network_range: 192.168.1.0
#    dhcp_proxy: true
#    tftp: true
#    tftp_root: /mnt/usb/tftpboot
#    pxe_service: 'X86PC,"PXE Boot...",pxelinux'
#    dns_enabled: true
#    port: 53
#    dns_upstream: 192.168.1.1
#    dns_domainname: houseofbears.co.uk
#    dns_statichosts: "/etc/dnsmasq_static_hosts.conf"#

#nginx_vars:
#  - nginx_service_name: nginx
#    nginx_port: 80
#    nginx_root: /mnt/usb/www/html#
#
#esxi_host:
#  - hostname: "esx1.houseofbears.co.uk"
#    macaddress: 34:17:eb:ba:2c:c1
#    ip_addr: 192.168.1.11
#    ip_subnetmask: 255.255.255.0
#    ip_gateway: 192.168.1.1
#    ip_nameserver: 192.168.1.1
#    major_version: "67"
#    minor_version: "u3"
#    tftp_root: /mnt/usb/tftpboot/
#    refresh: true
