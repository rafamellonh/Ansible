### Comandos 

```
ansible -i hosts all -u rafael -m ping
ansible -i hosts all -a "ls /etc"
ansible -i hosts all -m shell -a "/sbin/reboot" -b
ansible -i hosts all -m apt -a "update_cache=yes" -b
ansible -i hosts all -m apt -a "name=net-tools state=absent" -b
ansible -i hosts all -m systemd -a "name=ssh state=restarted" -b
ansible -i hosts all -m setup -a "filter=ansible_default_ipv4"
ansible -i hosts grupo01 -m setup -a "filter=ansible_default_ipv4"
ansible ubuntu01 -m debug -a var=http_port
```