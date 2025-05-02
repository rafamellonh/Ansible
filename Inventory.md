### Inventario

all : todos os target de nosso inventario
ungrouped : todos os targets que nao estao vinculados a um grupo no inventario

[Debian]
192.168.1.200

[redhat]
192.168.1.210

[windows]
192.168.1.[100:110]

[linux:children]
debian
redhat

[Debian] (dns)
debian01 ansible_host=192.168.1.200

[Debian] (user)
192.168.1.200 ansible_user=rafael

[linux:vars]
ansible_port=22
ansible_ssh_user=rafael
http_port=8080

### Inventario dinamico

* Configurar no azure : https://learn.microsoft.com/en-us/azure/developer/ansible/dynamic-inventory-configure?tabs=azure-cli
* ansible-config dump | grep INVENTORY_ENABLED
* Ativar o plugin no ansible.cfg
```  

[inventory]                                                                                                                                                                                                                              
enable_plugins          = aws_ec2, host_list, script, auto, yaml, ini, toml  

```