# PiMaster
## Pi Master node configuration  
This projects aim was to configure a Raspberry Pi from scratch (after base OS flashing of SD Card - with SSH and wifi configured) to act as a master control node for a Home Lab.

This home lab would be a single ESXi host deployed from PxE, configured by ansible to be accessed via a pfsense box, deploy VCSA and then nested virtual lab.

This repo currently:  
  -Deploys initial ansible user, homelab, to pi and gives it root  
  -Updates node  
  -Configures PxE with DNSMasq, TFTP, nginx and kickstart files and installs wake-on-lan  
  -Powers node on  
  -waits for install to complete (ping of node at end of install)  
  -Changes default boot option to local disk  

  You should now have a configured ESXi node, in eval mode, with SSH enabled.

## Prerequisites  
The following are required currently for this project:    
  
  - Linux desktop (currently only tested from Ubuntu 18.04.2)  
  - ESXi 6.7u3 ISO (needs to be extracted)  
  - VCSA ISO
  - Raspberry Pi (I am using a 3B+)
  - USB thumbdrive for Pi
  - Workstation or Server booting from USB
  - A metric ton of variables  
  - ovftool installed on local linux desktop

## Install - inital user creation
  

 - Create a user:  
   -  sudo useradd homelab
  - Add to sudo group (maybe not required but useful):
    - sudo usermod -aG sudo homelab  
  - Change terminal to homelab user:  
    -    sudo su - homelab
  - Generate ssh keys:
    - ssh-keygen -t rsa -b 4096  
  - Clone this repo  
    - git clone git@github.com:serokles/pimaster.git
  - Convert password to ansible "secure" string (should move to ansible vault in the future but this works for now and make sure you use the same password for the account when you created it):  
    - mkpasswd --method=SHA-512  
  - Copy the above value in to main.yml under roles/initial/vars under **homelab_password**  
  - Copy the ssh key in to the same file above under **pubkey** (this may be unnecessary now)  
  - Add IP address of your Pi to the inventory.ini  
  - Add IP address of your physical ESXi node under **homelab_esx**  
  - Configure SSH agent forwarding (needed for cloning git repos to PiMaster box later)  
    - eval "$(ssh-agent -s)"  
    - ssh-add ~/.ssh/id_rsa  
  - Scan keys in to known_hosts:
    - ssh-keyscan -H [IP of PiMaster] >> ~/.ssh/known_hosts
  -  Run the initial playbook to stage the homelab user to the Pi 
  -  This will prompt for the default pi user password 
     -  ansible-playbook initial.yml -l masternodes --ask-pass  
  
We should now have a Pi running and a user we can use on it.  The next step is to configure all the variables.  There are lots and there are some duplicates.  I have a shonky python script in this repo to generate them but otherwise just be careful to make sure you have copied, for example, the TFTP root path to all entries.  The table below should help:  

### usb_vars  
|Variable Name|Purpose| My Value|
|---|---|---|
| mount_path | Where you would like the USB stick on the Pi to be mounted. | /mnt/usb/ |  
  
### dnsmasq_vars  
|Variable Name|Purpose| My Value|
|---|---|---|  
| log | Enable logging | true |  
| network_range |What is the range of your existing LAN?  This is so that dnsmasq can operate in the same range to provide proxy PxE. | 192.168.1.0 |  
| dhcp_proxy | This set dnsmasq to proxy mode.  Not full DHCP so your home router can still server normal clients.  this will just add in the PxE settings for nodes that request it. | true |  
| tftp | Do you want TFTP enabled? Short answer is yes if you want ESXi installed. | true |  
| tftp_root | Where to place the root of your TFTP server? | /mnt/usb/tftpboot |  
| pxe_service | This sets the client system type, menu text and then the file to read from. | 'X86PC,"PXE Boot...",pxelinux' |  
| dns_enabled | Do you want to enable DNS? For the VCSA to function this should be true | true |  
| port | What port do you want DNS to operate on - default is 53 | 53 |  
| dns_upstream | When it cant answer a query where should a DNS query be sent? Most likely this is your home router address. | 192.168.1.1 |  
| dns_domainname | What do you want your homelab domain name to be? | houseofbears.co.uk |  
| dns_statichosts | This is a file that includes the static DNS entries for your homelab like the VCSA, physical ESXi etc etc | "/etc/dnsmasq_static_hosts.conf" |  

### nginx_vars  
|Variable Name|Purpose| My Value|
|---|---|---|  
| nginx_service_name | What do you want the service name to be?| nginx |  
| nginx_port | #what port do you want it to operate under? | 80 |
| nginx_root | What is the base directory that nginx will server web pages from? | "/mnt/usb/www/html" |  
  
### esxi_host  
|Variable Name|Purpose| My Value|
|---|---|---|  
| hostname | Hostname of your pyhsical ESXi host | "esx1.houseofbears.co.uk" |
| root_passwd | What should the root password be? | "VMware1!" |  
| macaddress | What is the MAC address of your physical host?  Needed for Wake On LAN | 34:17:eb:ba:2c:c1 |  
| ip_addr | ESXi host static IP | 192.168.1.11 |
| ip_subnetmask | Subnet mask for static IP | 255.255.255.0 |
| ip_gateway| Gateway for static IP.  Probably your home router IP.| 192.168.1.1 |
| ip_nameserver | Also probably your home router| 192.168.1.1 |
| major_version | This is for folder naming for PxE boot.  Added this so you could have multiple versions. | "67" |
| minor_version | See above. | "u3" |
| tftp_root | Where are the TFTP files for install? | /mnt/usb/tftpboot/ |
| refresh | This will force copies of file to the Pi.  Set to false if you are jus changing other setings like DNS names. | true |
| nginx_root | Where is nginx serving web pages from? | "/mnt/usb/www/html" |

### nfs_vars  
|Variable Name|Purpose| My Value|
|---|---|---|  
| nfs_root | Where do you want your NFS dir to be? | /mnt/usb/nfs |
| esx_ip_addr | What is the IP of your ESXi host?  This is for the exports file.| 192.168.1.11 |
| pfsense_ip_addr |  What is the IP of your pfsense VM WAN port?  This is for the exports file. | 192.168.1.12 |

### dns_entries  
|IP Address | Hostname| Purpose |  
|---|---|---|  
| 192.168.1.44 | pimaster.houseofbears.co.uk | Pi node that deploys installs and runs config scripts later. |  
| 192.168.1.11 | esx1.houseofbears.co.uk | Physical ESXi host. |  
| 192.168.1.12 | pfsense.houseofbears.co.uk | WAN IP address of pfsense VM.  WAN in this case is an IP on your home network. |  
| 10.64.0.20 | vcsa.houseofbears.co.uk | IP address of the VCSA.  This will be on the pfsense LAN segment. |

### network_vars  
|Variable Name|Purpose| My Value|
|---|---|---|  
| pfsense_ip | IP of pfsense WAN port | 192.168.1.12 |
| homelab_subnet | CIDR of homelab LAN | 16 |
| homelab_network| Network range of homelab LAN |10.64.0.0 |

## Run playbook  
Now all the variables are configured and the user is set you can run the following to configure the Pi, copy all the files, power on the host and install ESXi:  

      ansible-playbook site.yml -l masternodes -e "production=true"

## Results  

After the playbooks in this repo have run you should have the following:  

- ESXi installed on a physical host with an IP and specified root password.
- Pi configured with static route to proposed network for VMs.
- Clones of ESXi configuration repo and secret files specified.
- gov installed on Pi and ovftool deployed to ESXi host.  

This should be enough to play with vsphere but if you want the next stage then follow this repo:  

      https://github.com/serokles/pimaster-esxiconfig  

Which will configure the node and deploy the nested ESXi lab.




