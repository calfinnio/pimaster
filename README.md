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

