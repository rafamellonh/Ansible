
* arquivo hosts com os hosts valida o diretorio das variaveis :

/etc/ansible/host
```
[ubuntu01]
ubutnu01 ansible_host=192.168.1.220

[ubuntu02]
ubuntu02 ansible_host=192.168.1.221

[debian:children]
ubuntu01
ubuntu02
```


/etc/ansible/host_vars e /etc/ansible/groups_vars

* Group_vars
    * debian    (varialvel definida : port_ssh: 2222)
    * all
    * redhat
* host_vars
    * ubuntu01   (varialvel definida : http_port: 8080)
    * ubuntu02   (varialvel definida : http_port: 8081)
* criar dentro de hosts_vars um arquivo para cada host

ansible
├── ansible.cfg
├── group_vars
│   ├── all
│   ├── debian
│   └── redhat
├── hosts
├── hosts.original
├── host_vars
│   ├── ubuntu01
│   └── ubunt

